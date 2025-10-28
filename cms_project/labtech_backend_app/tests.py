from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Category


User = get_user_model()


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user with role = LabTechnician
        self.user = User.objects.create_user(
            username="labtech",
            password="password123",
            role="LabTechnician"
        )
        self.client = APIClient()
        self.client.login(username="labtech", password="password123")

        self.category = Category.objects.create(category_name="Blood Test")

    def test_list_categories(self):
        url = reverse("category-list")  # DRF router will create this
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        url = reverse("category-list")
        data = {"category_name": "Urine Test"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category(self):
        url = reverse("category-detail", args=[self.category.cat_id])
        data = {"category_name": "Updated Test"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        url = reverse("category-detail", args=[self.category.cat_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
