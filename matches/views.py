import json

from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from matches.models import Match, Turn, Move, Token, GameState
from matches.serializers import MatchSerializer, GameStateSerializer


class MatchViewSet(viewsets.ViewSet):
    """
    Endpoints for playing a match
    """
    queryset = Match.objects.all()

    def list(self, request):
        """
        List the matches the currently logged in user is in or has participated in
        """
        queryset = Match.objects.filter(Q(player_1=request.user.profile) | Q(player_2=request.user.profile))
        serializer = MatchSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Retrieves a particular match.
        """
        match = Match.objects.get(pk=pk)
        serializer = MatchSerializer(match, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        Put a list of moves here.
        Requires Player Token.
        Returns the updated Game State.
        """
        match = Match.objects.get(pk=pk)
        post = request.POST or json.loads(request.body)
        # check for token
        posted_token = post.get('token', False)
        if not posted_token:
            return Response(json.dumps({'error': 'user match token missing'}), status=status.HTTP_401_UNAUTHORIZED)
        if posted_token != Token.objects.get(match=match, profile=request.user.profile).uuid:
            return Response(json.dumps({'error': 'invalid user match token'}), status=status.HTTP_401_UNAUTHORIZED)
        # check if players current turn
        if request.user.profile is match.player_1 and match.get_turn_count() % 2 is not 1:
            return Response(json.dumps({'error': 'not your turn'}), status=status.HTTP_401_UNAUTHORIZED)
        if request.user.profile is match.player_2 and match.get_turn_count() % 2 is not 0:
            return Response(json.dumps({'error': 'not your turn'}), status=status.HTTP_401_UNAUTHORIZED)
        # execute moves
        moves = post.get('moves', [])
        turn = Turn.objects.get(match=match, number=match.get_turn_count(), profile="")
        for move in moves:
            Move.objects.create(turn=turn, )
        # increment turn
        next_turn = Turn.objects.create(match=match, profile="")
        next_turn.save()
        # update game state
        state = GameState.objects.get(match=match, profile=request.user.profile)

        serializer = GameStateSerializer(state, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @detail_route(methods=['GET'])
    def status(self, request, pk=None):
        """
        Returns the Current User and The Match's Current Turn.
        If user is logged in, it returns the user token.
        For Use in polling.
        """
        match = Match.objects.get(pk=pk)
        data = {
            "turn": match.get_turn_count(),
            "completed": match.completed,
        }
        if match.player_1 is request.user.profile:
            data['player'] = 1
        elif match.player_2 is request.user.profile:
            data['player'] = 2
        if match.player_1 is request.user.profile or match.player_2 is request.user.profile:
            token = Token.objects.get_or_create(
                match=match,
                profile=request.user.profile
            )
            data['token'] = token.uuid
        return Response(json.dumps(data), status.HTTP_200_OK)