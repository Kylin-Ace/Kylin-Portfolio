from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import BlogPost, ContactMessage, Project


class PortfolioPageTests(TestCase):
    def test_home_and_projects_pages_render(self):
        Project.objects.create(title="A useful tool", description="A small project.")

        self.assertEqual(self.client.get(reverse("myapp:home")).status_code, 200)
        response = self.client.get(reverse("myapp:projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A useful tool")

    def test_blog_search_returns_published_posts_only(self):
        BlogPost.objects.create(
            title="Python automation",
            slug="python-automation",
            content="Practical Python notes.",
            image="blog/python.jpg",
            status=BlogPost.PUBLISHED,
            published_at=timezone.now(),
        )
        BlogPost.objects.create(
            title="Python draft",
            slug="python-draft",
            content="A draft that should stay private.",
            image="blog/draft.jpg",
        )

        response = self.client.get(reverse("myapp:blog"), {"q": "python"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python automation")
        self.assertNotContains(response, "Python draft")

    def test_contact_submission_is_saved(self):
        response = self.client.post(
            reverse("myapp:contact"),
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "subject": "A project idea",
                "message": "Could we work together?",
            },
        )

        self.assertRedirects(response, reverse("myapp:contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.get().email, "ada@example.com")
