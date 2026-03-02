import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from users.factories import UserFactory, TrainerFactory
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def trainer_client(api_client):
    trainer = TrainerFactory()
    api_client.force_authenticate(user=trainer)
    return api_client, trainer


@pytest.mark.django_db
class TestRegistration:
    """Test for user registration endpoint."""

    def test_register_success(self, api_client):
        """Test successful registration."""
        url = reverse("auth:register")
        data = {
            "username": "testuser",
            "email": "test@mail.com",
            "password": "SecurePass123:",
            "password_confirm": "SecurePass123:",
            "first_name": "test",
            "last_name": "test",
            "is_trainer": False,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "tokens" in response.data
        assert "access" in response.data["tokens"]
        assert "refresh" in response.data["tokens"]
        assert response.data["user"]["username"] == "testuser"
        assert User.objects.filter(username="testuser").exists()

    def test_register_password_mismatch(self, api_client):
        """Test registration fails when password don't match."""
        url = reverse("auth:register")
        data = {
            "username": "testuser",
            "email": "test@mail.com",
            "password": "SecurePass123:",
            "password_confirm": "SecurePass321:",
            "first_name": "test",
            "last_name": "test",
            "is_trainer": False,
        }

        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password_confirm" in response.data

    def test_register_duplicate_email(self, api_client):
        """Test registration fails when email is already exist."""
        UserFactory(email="test1@mail.com")

        url = reverse("auth:register")
        data = {
            "username": "testuser",
            "email": "test1@mail.com",
            "password": "SecurePass123:",
            "password_confirm": "SecurePass123:",
            "first_name": "test",
            "last_name": "test",
            "is_trainer": False,
        }

        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_register_duplicate_username(self, api_client):
        """Test registration fails when username is already exist."""
        UserFactory(username="test1")

        url = reverse("auth:register")
        data = {
            "username": "test1",
            "email": "test2@mail.com",
            "password": "SecurePass123:",
            "password_confirm": "SecurePass123:",
            "first_name": "test",
            "last_name": "test",
            "is_trainer": False,
        }

        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_register_as_trainer(self, api_client):
        """Test register as a trainer."""
        url = reverse("auth:register")
        data = {
            "username": "testuser",
            "email": "tes31@mail.com",
            "password": "SecurePass123:",
            "password_confirm": "SecurePass123:",
            "first_name": "test",
            "last_name": "test",
            "is_trainer": True,
        }

        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["is_trainer"] is True
