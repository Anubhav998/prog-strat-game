import json

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from matches.models import Match, Turn, Action, GameState, Token, ResourceState, MilitaryState, TechnologyState, \
    TerritoryState, ReligionState, ConflictState
from resources.models import Resource
from military.models import Unit, Category
from sciences.models import Technology
from arenas.models import Arena, Territory
from combat.models import Conflict


class MatchTestCase(TestCase):
    fixtures = ['resources', 'actions', 'technologies']

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.user2 = User.objects.create_user(username='user2')
        self.arena = Arena.objects.create(name='Small', size_x=5, size_y=5, created_by=self.user1)
        self.match = Match.objects.create(
            arena=self.arena,
            player_1=self.user1.profile,
            player_2=self.user2.profile
        )

    def test_match_unicode_method(self):
        self.assertEquals(self.match.__unicode__(), "user1.vs.user2")

    def test_match_get_turn_count_method(self):
        self.assertEquals(self.match.get_turn_count(), 1)

    def test_match_get_player_method(self):
        self.assertEquals(self.match.get_player(1), self.user1.profile)
        self.assertEquals(self.match.get_player(2), self.user2.profile)

    def test_match_clean_method(self):
        self.invalid_match = Match()
        self.invalid_match.arena = self.arena
        self.invalid_match.player_1 = self.user1.profile
        self.invalid_match.player_2 = self.user1.profile
        self.assertRaises(ValidationError, self.invalid_match.clean)
        self.invalid_match.player_2 = self.user2.profile
        self.invalid_match.completed = True
        self.assertRaises(ValidationError, self.invalid_match.clean)

    def test_turn_unicode_method(self):
        self.assertEquals(self.match.get_current_turn().__unicode__(), "user1.vs.user2 Turn 1")

    def test_action_unicode_method(self):
        self.action = Action.objects.create(name='test')
        self.assertEquals(self.action.__unicode__(), 'test')

    def test_game_state_unicode_method(self):
        self.game_state = GameState.objects.get(
            match=self.match,
            player=1
        )
        self.assertEquals(self.game_state.__unicode__(), "user1.vs.user2 Game State 1")

    def test_token_unicode(self):
        self.token = Token.objects.create(
            match=self.match,
            profile=self.user1.profile
        )
        self.assertNotEqual(self.token.__unicode__(), "")

    def test_resource_state_unicode_method(self):
        self.game_state = GameState.objects.get(
            match=self.match,
            player=1
        )
        self.resource = Resource.objects.create(name='test')
        self.resource_state = ResourceState.objects.create(
            state=self.game_state,
            resource=self.resource
        )
        self.assertEquals(self.resource_state.__unicode__(), "Resource State %s" % self.resource_state.id)

    def test_military_state_unicode_method(self):
        self.game_state = GameState.objects.get(
            match=self.match,
            player=1
        )
        self.category = Category.objects.create(name='test1'
                                                )
        self.unit = Unit.objects.create(name='test', category=self.category)
        self.military_state = MilitaryState.objects.create(
            state=self.game_state,
            unit=self.unit
        )
        self.assertEquals(self.military_state.__unicode__(), "Military State %s" % self.military_state.id)

    def test_military_state_clean_method(self):
        self.game_state = GameState.objects.get(
            match=self.match,
            player=1
        )
        self.category = Category.objects.create(name='test1'
                                                )
        self.unit = Unit.objects.create(name='test', category=self.category)
        self.military_state = MilitaryState.objects.create(
            state=self.game_state,
            unit=self.unit
        )
        self.military_state.quantity -= 10
        self.assertRaises(ValidationError, self.military_state.clean)

    def test_technology_state_unicode_method(self):
        self.game_state = GameState.objects.get(
            match=self.match,
            player=1
        )
        self.technology = Technology.objects.create(name='test')
        self.technology_state = TechnologyState.objects.create(
            state=self.game_state,
            technology=self.technology
        )
        self.assertEquals(self.technology_state.__unicode__(), "Technology State %s" % self.technology_state.id)

    def test_territory_state_unicode_method(self):
        self.game_state = GameState.objects.get(
            match=self.match,
            player=1
        )
        self.territory = Territory.objects.filter(arena=self.arena).first()
        self.territory_state = TerritoryState.objects.create(
            state=self.game_state,
            territory=self.territory
        )
        self.assertEquals(self.territory_state.__unicode__(), "Territory State %s" % self.territory_state.id)

    def test_religion_state_unicode_method(self):
        self.game_state = GameState.objects.get(
            match=self.match,
            player=1
        )
        self.religion_state = ReligionState.objects.create(
            state=self.game_state,
        )
        self.assertEquals(self.religion_state.__unicode__(), "Faith State %s" % self.religion_state.id)

    def test_conflict_state_unicode_method(self):
        self.game_state = GameState.objects.get(
            match=self.match,
            player=1
        )
        self.conflict = Conflict.objects.create(
            territory=self.arena.territory_set.first(),
            aggressor=self.user1.profile,
            defender=self.user2.profile,
            start_turn=1
        )
        self.conflict_state = ConflictState.objects.create(
            state=self.game_state,
            conflict=self.conflict
        )
        self.assertEquals(self.conflict_state.__unicode__(), "Conflict State %s" % self.conflict_state.id)


class MatchesAPITestCase(APITestCase):
    fixtures = ['resources', 'actions', 'technologies']

    def setUp(self):
        self.user1 = User.objects.create_superuser(username='user1', email='test@test.com', password='test')
        self.user2 = User.objects.create_user(username='user2')
        self.arena = Arena.objects.create(name='Small', size_x=5, size_y=5, created_by=self.user1)
        self.match = Match.objects.create(
            arena=self.arena,
            player_1=self.user1.profile,
            player_2=self.user2.profile
        )
        auth = self.client.login(username='user1', password='test')
        self.assertTrue(auth)

    def test_get_match_list(self):
        url = reverse('match-list')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_match_retrieve(self):
        url = reverse('match-detail', args=(self.match.uuid,))
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_match_status(self):
        url = reverse('match-status', args=(self.match.uuid,))
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.data)
        self.assertEquals(data['completed'], False)
        self.assertEquals(data['player'], 1)
        self.assertEquals(data['turn'], 1)

    def test_get_match_turn_2(self):
        self.turn1 = self.match.get_current_turn()
        self.turn1.completed = True
        self.turn1.save()
        self.match.turns.all()
        self.turn2 = Turn.objects.create(
            match=self.match,
            profile=self.user2.profile,
            number=2
        )
        url = reverse('match-status', args=(self.match.uuid,))
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.data)
        self.assertEquals(data['completed'], False)
        self.assertEquals(data['player'], 2)
        self.assertEquals(data['turn'], 2)

    def test_get_match_state(self):
        url = reverse('match-state', args=(self.match.uuid,))
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_match_state_wrong_user(self):
        client = Client()
        User.objects.create_user(username='user3', password='test')
        client.login(username='user3', password='test')
        url = reverse('match-state', args=(self.match.uuid,))
        response = client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(response.data)['error'], 'not game player')

    def test_get_match_list_not_logged_in(self):
        client = Client()
        url = reverse('match-list')
        response = client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(response.data)['error'], 'you must be logged in')

    def test_get_match_state_not_logged_in(self):
        client = Client()
        url = reverse('match-state', args=(self.match.uuid,))
        response = client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(response.data)['error'], 'you must be logged in')


class MatchPlayTestCase(TestCase):
    fixtures = ['resources', 'actions', 'technologies', 'military']

    def setUp(self):
        # player 1 setup
        self.client1 = Client()
        self.user1 = User.objects.create_superuser(username='user1', email='test@test.com', password='test')
        auth1 = self.client1.login(username='user1', password='test')
        self.assertTrue(auth1)
        # player 2 setup
        self.client2 = Client()
        self.user2 = User.objects.create_superuser(username='user2', email='test2@test.com', password='test')
        auth2 = self.client2.login(username='user2', password='test')
        self.assertTrue(auth2)
        # setup game
        self.arena = Arena.objects.create(name='Small', size_x=5, size_y=5, created_by=self.user1)
        self.match = Match.objects.create(
            arena=self.arena,
            player_1=self.user1.profile,
            player_2=self.user2.profile
        )

    def test_game_play(self):
        # define urls
        status_url = reverse('match-status', args=(self.match.uuid,))
        match_url = reverse('match-detail', args=(self.match.uuid,))
        state_url = reverse('match-state', args=(self.match.uuid,))

        # player status check
        player_1_response_1 = self.client1.get(status_url, format='json')
        self.assertEquals(player_1_response_1.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_1_response_1.data)['turn'], 1)
        player_1_token = json.loads(player_1_response_1.data)['token']
        player_2_response_1 = self.client2.get(status_url, format='json')
        self.assertEquals(player_2_response_1.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_2_response_1.data)['turn'], 1)
        player_2_token = json.loads(player_2_response_1.data)['token']

        # different user tokens
        self.assertNotEqual(
            json.loads(player_1_response_1.data)['token'],
            json.loads(player_2_response_1.data)['token']
        )

        # player one put without token fails
        data_1 = {"moves": []}
        player_1_response_2 = self.client1.put(match_url, json.dumps(data_1), format='json')
        self.assertEquals(player_1_response_2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(player_1_response_2.data)['error'], "user match token missing")

        # player 2 update fails
        data_2 = {
            "token": player_2_token,
            "moves": []
        }
        player_2_response_2 = self.client2.put(match_url, json.dumps(data_2), format=json)
        self.assertEquals(player_2_response_2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(player_2_response_2.data)['error'], "invalid user match token")

        # player 1 puts invalid moves update
        data_3 = {
            "token": player_1_token,
            "moves": [
                {}
            ]
        }
        player_1_response_3 = self.client1.put(match_url, json.dumps(data_3), format='json')
        self.assertEquals(player_1_response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_1_response_3.data)['error'], 'invalid turn')

        # player 1 puts valid move
        data_4 = {
            "token": player_1_token,
            "moves": [
                {
                    "action": "Purchase",
                    "object": "Soldier",
                    "quantity": 9
                }
            ]
        }
        player_1_response_4 = self.client1.put(match_url, json.dumps(data_4), format='json')
        self.assertEquals(player_1_response_4.status_code, status.HTTP_202_ACCEPTED)

        # player status gets
        player_1_response_5 = self.client1.get(status_url, format='json')
        self.assertEquals(player_1_response_5.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_1_response_5.data)['turn'], 2)
        player_2_response_3 = self.client2.get(status_url, format='json')
        self.assertEquals(player_2_response_3.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_2_response_3.data)['turn'], 2)

        # player 1 put is rejected
        data_5 = {
            "token": player_1_token,
            "moves": []
        }
        player_1_response_6 = self.client1.put(match_url, json.dumps(data_5), format=json)
        self.assertEquals(player_1_response_6.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(json.loads(player_1_response_6.data)['error'], "invalid user match token")

        # player 2 puts invalid move
        data_6 = {
            "token": player_2_token,
            "moves": [
                {
                    "action": "Purchase",
                    "object": "Soldier",
                    "quantity": 11
                }
            ]
        }
        player_2_response_4 = self.client2.put(match_url, json.dumps(data_6), format='json')
        self.assertEquals(player_2_response_4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_2_response_4.data)['error'], 'invalid turn')

        # player 2 puts valid move
        data_7 = {
            "token": player_2_token,
            "moves": [
                {
                    "action": "Refine",
                    "object": "Steel",
                    "quantity": 10
                },
                {
                    "action": "Research",
                    "object": "Concrete",
                    "quantity": 1
                },
                {
                    "action": "Purchase",
                    "object": "Soldier",
                    "quantity": 1
                }
            ]
        }
        player_2_response_5 = self.client2.put(match_url, json.dumps(data_7), format='json')
        self.assertEquals(player_2_response_5.status_code, status.HTTP_202_ACCEPTED)
        data = player_2_response_5.data
        self.assertEquals(data.get('resources')[0].get('quantity'), 400 + 100)  # fuel + income
        self.assertEquals(data.get('resources')[1].get('quantity'), 400 + 100)  # metal + income
        self.assertEquals(data.get('resources')[2].get('quantity'), 200 + 250)  # manpower + income
        self.assertEquals(data.get('resources')[3].get('quantity'), 10)  # steel
        self.assertEquals(data.get('technology')[0].get('acquired'), True)
        self.assertEquals(data.get('military')[0].get('quantity'), 1)

        # player status check
        player_1_response_7 = self.client1.get(status_url, format='json')
        self.assertEquals(player_1_response_7.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_1_response_7.data)['turn'], 3)
        player_2_response_6 = self.client2.get(status_url, format='json')
        self.assertEquals(player_2_response_6.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_2_response_6.data)['turn'], 3)

        # player 1 prays
        data_8 = {
            "token": player_1_token,
            "moves": [
                {
                    "action": "Pray",
                    "object": "Faith",
                    "quantity": 10
                }
            ]
        }
        player_1_response_8 = self.client1.put(match_url, json.dumps(data_8), format='json')
        self.assertEquals(player_1_response_8.status_code, status.HTTP_202_ACCEPTED)
        data = player_1_response_8.data
        self.assertEquals(data.get('religion')[0].get('amount'), 10)  # faith
        self.assertEquals(data.get('military')[0].get('quantity'), 9)  # soldiers
        self.assertEquals(data.get('resources')[0].get('quantity'), 700)  # fuel
        self.assertEquals(data.get('resources')[1].get('quantity'), 700)  # metal
        self.assertEquals(data.get('resources')[2].get('quantity'), 590)  # manpower

        # player status check
        player_1_response_9 = self.client1.get(status_url, format='json')
        self.assertEquals(player_1_response_9.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_1_response_9.data)['turn'], 4)
        player_2_response_7 = self.client2.get(status_url, format='json')
        self.assertEquals(player_2_response_7.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_2_response_7.data)['turn'], 4)

        # player 2 tires to purchase without proper technology, but with proper resources
        data_9 = {
            "token": player_2_token,
            "moves": [
                {
                    "action": "Refine",
                    "object": "Titanium",
                    "quantity": 1
                }
            ]
        }
        player_2_response_8 = self.client2.put(match_url, json.dumps(data_9), format='json')
        self.assertEquals(player_2_response_8.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_2_response_8.data).get('detail'), 'insufficient technology: Alloys')

        # player 2 tries to purchase a tank without proper technology
        data_10 = {
            "token": player_2_token,
            "moves": [
                {
                    "action": "Purchase",
                    "object": "Tank",
                    "quantity": 1
                }
            ]
        }
        player_2_response_9 = self.client2.put(match_url, json.dumps(data_10), format='json')
        self.assertEquals(player_2_response_9.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_2_response_9.data).get('detail'), 'insufficient technology: Vehicles')

        # player 2 tries to research advanced vehicles without dependency
        data_11 = {
            "token": player_2_token,
            "moves": [
                {
                    "action": "Research",
                    "object": "Advanced Vehicles",
                    "quantity": 1
                }
            ]
        }
        player_2_response_10 = self.client2.put(match_url, json.dumps(data_11), format='json')
        self.assertEquals(player_2_response_10.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_2_response_10.data).get('detail'), 'insufficient technology: Vehicles')

        # player 2 submits a blank move set
        data_12 = {
            "token": player_2_token,
            "moves": []
        }
        player_2_response_11 = self.client2.put(match_url, json.dumps(data_12), format='json')
        self.assertEquals(player_2_response_11.status_code, status.HTTP_202_ACCEPTED)
        data = player_2_response_11.data
        self.assertEquals(data.get('resources')[0].get('quantity'), 500 + 100)  # fuel + income
        self.assertEquals(data.get('resources')[1].get('quantity'), 500 + 100)  # metal + income
        self.assertEquals(data.get('resources')[2].get('quantity'), 450 + 250)  # manpower + income
        self.assertEquals(data.get('resources')[3].get('quantity'), 10)  # steel
        self.assertEquals(data.get('technology')[0].get('acquired'), True)
        self.assertEquals(data.get('military')[0].get('quantity'), 1)

        # player status check
        player_1_response_10 = self.client1.get(status_url, format='json')
        self.assertEquals(player_1_response_10.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_1_response_10.data)['turn'], 5)
        player_2_response_12 = self.client2.get(status_url, format='json')
        self.assertEquals(player_2_response_12.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(player_2_response_12.data)['turn'], 5)

        # player 1 comes back to game and checks state
        player_1_response_11 = self.client1.get(state_url, format='json')
        data = player_1_response_11.data
        self.assertEquals(data.get('religion')[0].get('amount'), 10)  # faith
        self.assertEquals(data.get('military')[0].get('quantity'), 9)  # soldiers
        self.assertEquals(data.get('resources')[0].get('quantity'), 700)  # fuel
        self.assertEquals(data.get('resources')[1].get('quantity'), 700)  # metal
        self.assertEquals(data.get('resources')[2].get('quantity'), 590)  # manpower

        # player 1 tries using invalid resource name
        data_13 = {
            "token": player_1_token,
            "moves": [
                {
                    "action": "Refine",
                    "object": "invalid",
                    "quantity": 1
                }
            ]
        }
        player_1_response_12 = self.client1.put(match_url, json.dumps(data_13), format='json')
        self.assertEquals(player_1_response_12.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_1_response_12.data).get('detail'), 'invalid resource name: "invalid"')

        # player 1 tries using invalid unit name
        data_14 = {
            "token": player_1_token,
            "moves": [
                {
                    "action": "Purchase",
                    "object": "invalid",
                    "quantity": 1
                }
            ]
        }
        player_1_response_13 = self.client1.put(match_url, json.dumps(data_14), format='json')
        self.assertEquals(player_1_response_13.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_1_response_13.data).get('detail'), 'invalid unit name: "invalid"')

        # player 1 tries using invalid technology name
        data_15 = {
            "token": player_1_token,
            "moves": [
                {
                    "action": "Research",
                    "object": "invalid",
                    "quantity": 1
                }
            ]
        }
        player_1_response_14 = self.client1.put(match_url, json.dumps(data_15), format='json')
        self.assertEquals(player_1_response_14.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_1_response_14.data).get('detail'), 'invalid technology name: "invalid"')

        # player 1 tries uses invalid action name
        data_16 = {
            "token": player_1_token,
            "moves": [
                {
                    "action": "invalid",
                    "object": "Soldier",
                    "quantity": 1
                }
            ]
        }
        player_1_response_15 = self.client1.put(match_url, json.dumps(data_16), format='json')
        self.assertEquals(player_1_response_15.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(player_1_response_15.data).get('detail'), 'action not found')
