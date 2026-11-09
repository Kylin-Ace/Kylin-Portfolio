from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Listing


class ListingAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_user_model()
        cls.owner = users.objects.create_user(username="owner")
        cls.other_user = users.objects.create_user(username="other")
        cls.token = Token.objects.create(user=cls.owner)
        cls.listing = Listing.objects.create(
            owner=cls.owner, title="Desk lamp", price="12.50"
        )
        cls.other_listing = Listing.objects.create(
            owner=cls.other_user, title="Textbook", price="20.00"
        )

    def setUp(self):
        self.url = reverse("listing-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_collection_returns_only_owned_listings(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.listing.pk])

    def test_another_users_listing_cannot_be_read_or_changed(self):
        url = reverse("listing-detail", args=[self.other_listing.pk])
        requests = [
            ("get", {}),
            ("put", {"data": {"title": "Changed", "price": "10.00"}, "format": "json"}),
            ("patch", {"data": {"title": "Changed"}, "format": "json"}),
            ("delete", {}),
        ]
        for method, kwargs in requests:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, **kwargs)
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_listing.refresh_from_db()
        self.assertEqual(self.other_listing.title, "Textbook")

    def test_create_derives_owner_from_token(self):
        response = self.client.post(
            self.url,
            {"title": "Chair", "price": "25.00", "owner": self.other_user.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        listing = Listing.objects.get(pk=response.data["id"])
        self.assertEqual(listing.owner, self.owner)
        self.assertEqual(listing.status, Listing.Status.DRAFT)

    def test_invalid_fields_are_rejected(self):
        response = self.client.post(
            self.url,
            {"title": "  ", "price": "-1", "status": "unknown"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data), {"title", "price", "status"})

    def test_owner_can_update_and_delete_listing(self):
        url = reverse("listing-detail", args=[self.listing.pk])
        response = self.client.patch(url, {"status": "active"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], Listing.Status.ACTIVE)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Listing.objects.filter(pk=self.listing.pk).exists())
