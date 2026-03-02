from django.test import TestCase

from users.factories import UserFactory
from users.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser", email="example@mail.com", bio="Test bio")

    def test_user_serializer(self):
        """Test serializing a user."""
        serializer = UserSerializer(self.user)
        data = serializer.data

        self.assertEqual(data["id"], self.user.pk)
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "example@mail.com")
        self.assertEqual(data["bio"], "Test bio")
