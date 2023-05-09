from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError

from users.models import User


class TestAuth(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_credentials = {'username': 'user', 'confirmation_code': '1234567890'}

        user = User.objects.create_user(**cls.user_credentials)

    def setUp(self):
        super().setUp()

    def test_admin_create_user(self):
        pass

    def test_user_signup(self):
        pass

    def test_auth_can_obtain_token_with_valid_credentials(self):
        response = self.client.post(reverse('api:get_token'), self.user_credentials, format='json')

        self.assertEquals(response.status_code, 200)
        json = response.json()
        self.assertIn('token', json)
        token = json['token']
        try:
            UntypedToken(token)
            error_message = ''
        except TokenError as error:
            error_message = str(error)

        self.assertTrue(error_message == '', f'{error_message}')

    def test_auth_can_not_obtain_token_with_invalid_credentials(self):

        cases = (
            ({}, 400),
            ({'username': 'asd'}, 400),
            ({'confirmation_code': '12345'}, 400),
            ({'username': 'asd', 'confirmation_code': '12345'}, 404),
        )

        for credentials, code in cases:
            with self.subTest(data=credentials):
                response = self.client.post(reverse('api:get_token'), credentials, format='json')
                self.assertTrue(response.status_code, code)
