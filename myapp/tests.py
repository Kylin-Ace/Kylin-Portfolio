from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import BlogPost


class PublicBlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.draft = BlogPost.objects.create(
            title='Draft post',
            content='Draft content.',
            image='blog/draft.jpg',
        )
        cls.published = BlogPost.objects.create(
            title='Published post',
            content='Published content.',
            image='blog/published.jpg',
            status=BlogPost.PUBLISHED,
            published_at=timezone.now(),
        )

    def test_index_lists_only_published_posts(self):
        response = self.client.get(reverse('myapp:blog'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['posts'], [self.published])

    def test_draft_detail_returns_404(self):
        response = self.client.get(self.draft.get_absolute_url())

        self.assertEqual(response.status_code, 404)

    def test_published_detail_renders_post(self):
        response = self.client.get(self.published.get_absolute_url())

        self.assertContains(response, self.published.content)

    def test_admin_can_publish_an_existing_draft(self):
        admin_user = get_user_model().objects.create_superuser(
            username='editor',
            password='local-test-password',
        )
        self.client.force_login(admin_user)
        response = self.client.post(
            reverse('admin:myapp_blogpost_change', args=[self.draft.pk]),
            {
                'title': self.draft.title,
                'slug': self.draft.slug,
                'content': self.draft.content,
                'status': BlogPost.PUBLISHED,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.draft.refresh_from_db()
        self.assertIsNotNone(self.draft.published_at)
        self.client.logout()
        self.assertContains(
            self.client.get(self.draft.get_absolute_url()),
            self.draft.content,
        )
