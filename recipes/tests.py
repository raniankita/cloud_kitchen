from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Recipe


class RecipesAPITest(APITestCase):
	def setUp(self):
		self.User = get_user_model()
		self.user1 = self.User.objects.create_user(username='u1', password='pass1234')
		self.user2 = self.User.objects.create_user(username='u2', password='pass1234')

	def test_create_recipe_assigns_user(self):
		self.client.force_authenticate(user=self.user1)
		url = '/api/recipes/'
		data = {
			'name': 'Test Recipe',
			'description': 'Tasty',
			'instructions': 'Mix and cook',
			'prep_time': 10,
			'cook_time': 20,
			'servings': 2
		}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Recipe.objects.count(), 1)
		recipe = Recipe.objects.first()
		self.assertEqual(recipe.user, self.user1)

	def test_list_only_returns_user_recipes(self):
		Recipe.objects.create(user=self.user1, name='R1', instructions='a', prep_time=1, cook_time=1, servings=1)
		Recipe.objects.create(user=self.user2, name='R2', instructions='b', prep_time=1, cook_time=1, servings=1)
		self.client.force_authenticate(user=self.user1)
		resp = self.client.get('/api/recipes/')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(len(resp.data), 1)
		self.assertEqual(resp.data[0]['name'], 'R1')

	def test_cannot_edit_other_users_recipe(self):
		recipe = Recipe.objects.create(user=self.user2, name='Other', instructions='x', prep_time=1, cook_time=1, servings=1)
		self.client.force_authenticate(user=self.user1)
		url = f'/api/recipes/{recipe.id}/'
		data = {'name': 'Hacked', 'instructions': 'x', 'prep_time':1, 'cook_time':1, 'servings':1}
		resp = self.client.put(url, data, format='json')
		# The viewset restricts queryset to the requesting user's recipes,
		# so attempting to access another user's recipe returns 404 Not Found.
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
