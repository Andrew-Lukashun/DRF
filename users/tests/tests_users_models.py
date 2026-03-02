from django.test import TestCase
from users.factories import UserFactory, TrainerFactory
from users.models import User


class UserModelsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.trainer = TrainerFactory()

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertIsNotNone(self.user.pk)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_trainer)

    def test_trainer_creation(self):
        self.assertIsInstance(self.trainer, User)
        self.assertIsNotNone(self.trainer.pk)
        self.assertFalse(self.trainer.is_staff)
        self.assertTrue(self.trainer.is_trainer)

    def test_user_str_representation(self):
        user = UserFactory(username="test_user")
        self.assertEqual(str(user), "test_user")

    def test_trainer_str_representation(self):
        trainer = TrainerFactory(username="test_trainer")
        self.assertEqual(str(trainer), "test_trainer")


class UserPropertiesTestCase(TestCase):
    def test_full_name_with_first_name_and_last_name(self):
        user = UserFactory(first_name="John", last_name="Doe")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.full_name, "John Doe")

    def test_full_name_without_last_name(self):
        user = UserFactory(first_name="John", last_name="")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "")
        self.assertEqual(user.full_name, "John")


class UserAuthTestCase(TestCase):
    def test_user_password_is_hashed(self):
        user = UserFactory(password="1234")
        self.assertNotEqual(user.password, "1234")
        self.assertTrue(user.check_password("1234"))

    def test_user_can_authenticate(self):
        user = UserFactory(password="1234")
        self.assertTrue(user.check_password("1234"))

    def test_user_can_not_authenticate(self):
        user = UserFactory(password="1234")
        self.assertFalse(user.check_password("4321"))
