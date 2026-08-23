from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


class UsersAPITest(APITestCase):
	def setUp(self):
		self.User = get_user_model()

	def test_signup_creates_user(self):
		url = '/api/users/signup/'
		data = {
			'username': 'testuser',
			'email': 'test@example.com',
			'password': 'StrongPassw0rd!',
			'is_customer': True
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(self.User.objects.filter(username='testuser').exists())

	def test_token_obtain_pair(self):
		# create user
		user = self.User.objects.create_user(username='loginuser', email='login@example.com', password='Pass12345')
		url = '/api/users/token/'
		data = {'username': 'loginuser', 'password': 'Pass12345'}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data)
		self.assertIn('refresh', response.data)

	def test_profile_requires_auth_and_returns_user(self):
		user = self.User.objects.create_user(username='profuser', email='prof@example.com', password='ProfPass1')
		# unauthenticated should be denied
		url = '/api/users/profile/'
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

		# authenticate and fetch profile
		self.client.force_authenticate(user=user)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.data.get('username'), 'profuser')
