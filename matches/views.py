import json

from django.db.models import Q
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from matches.models import Match, Turn, Move, Token, GameState, Action
from matches.serializers import MatchSerializer, GameStateSerializer


class MatchViewSet(viewsets.ViewSet):
    """
    Endpoints for playing a match
    """
    queryset = Match.objects.all()
    lookup_field = 'uuid'

    def list(self, request):
        """
        List the matches the currently logged in user is in or has participated in
        """
        if not request.user.is_authenticated():
            return Response(json.dumps({'error': 'you must be logged in'}), status=status.HTTP_401_UNAUTHORIZED)
        queryset = Match.objects.filter(Q(player_1=request.user.profile) | Q(player_2=request.user.profile))
        serializer = MatchSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, uuid=None):
        """
        Retrieves a particular match.
        """
        match = Match.objects.get(uuid=uuid)
        serializer = MatchSerializer(match, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, uuid=None):
        """
        Put a list of moves here.
        Requires Player Token.
        Returns the updated Game State.
        """
        match = Match.objects.get(uuid=uuid)
        turn = match.get_current_turn()
        post = request.POST or json.loads(request.body)
        # check for token
        posted_token = post.get('token', False)
        if not posted_token:
            return Response(json.dumps({'error': 'user match token missing'}), status=status.HTTP_401_UNAUTHORIZED)
        turn_token = str(Token.objects.get(match=match, profile=turn.profile))
        if posted_token != turn_token:
            return Response(json.dumps({'error': 'invalid user match token'}), status=status.HTTP_401_UNAUTHORIZED)
        # execute moves
        moves = post.get('moves', [])
        for move in moves:
            try:
                action = Action.objects.get(name=move.get('action'))
            except ObjectDoesNotExist:
                return Response(json.dumps({'error': 'invalid turn'}), status=status.HTTP_400_BAD_REQUEST)
            Move.objects.create(turn=turn, action=action, object=move.get('object'), quantity=move.get('quantity'))
        # update game state
        state = GameState.objects.get(match=match, profile=request.user.profile)
        try:
            state.apply_turn(turn, commit=False)
            state.apply_turn(turn, commit=True)
        except ValidationError:
            for move in turn.moves.all():
                move.delete()
            return Response(json.dumps({'error': 'invalid turn'}), status=status.HTTP_400_BAD_REQUEST)
        # increment turn
        opponent = match.player_1 if request.user.profile == match.player_2 else match.player_2
        Turn.objects.create(match=match, profile=opponent, number=turn.number + 1)
        # return the new game state
        serializer = GameStateSerializer(state, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @detail_route(methods=['GET'])
    def status(self, request, uuid=None):
        """
        Returns the Current User and The Match's Current Turn.
        If user is logged in, it returns the user token.
        For Use in polling.

        :param request: Request Object
        :param uuid: UUID of the match
        :return: Response of a status object
        """
        match = Match.objects.get(uuid=uuid)
        turn = match.get_current_turn()
        data = {
            "turn": turn.number,
            "completed": match.completed,
        }
        if match.player_1 == turn.profile:
            data['player'] = 1
        elif match.player_2 == turn.profile:
            data['player'] = 2
        if match.player_1 == request.user.profile or match.player_2 == request.user.profile:
            token, _ = Token.objects.get_or_create(
                match=match,
                profile=request.user.profile
            )
            data['token'] = str(token.uuid)
        return Response(json.dumps(data), status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def state(self, request, uuid=None):
        """helper method to get the current gamestate without putting new data

        :param request: Request object
        :param uuid: UUID of the match
        :return: Response object of serialized gamestate
        """
        if not request.user.is_authenticated():
            return Response(json.dumps({'error': 'you must be logged in'}), status=status.HTTP_401_UNAUTHORIZED)
        match = Match.objects.get(uuid=uuid)
        if match.player_1 == request.user.profile or match.player_2 == request.user.profile:
            game_state = GameState.objects.get(match=match, profile=request.user.profile)
            serializer = GameStateSerializer(game_state, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(json.dumps({'error': 'not game player'}), status=status.HTTP_401_UNAUTHORIZED)
