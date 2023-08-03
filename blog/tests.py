from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import Post


class PostManagersTest(TestCase):
    def test_create_post(self):
        user = get_user_model().objects.create_user(
            username="testuser", email="testuser@dummy.com", password="qwe123QWE!@#"
        )
        post = Post.objects.create(user=user, title="test", description="test desc")
        self.assertEqual(post.title, "test")
        self.assertEqual(post.description, "test desc")
        self.assertEqual(post.user, user)
        self.assertFalse(post.comment_set.count())
        self.assertEqual(post.updated_at, post.created_at)
        self.assertTrue(post.approved)
        self.assertFalse(post.is_published)
        post.title = "test1"
        post.save()
        self.assertNotEquals(post.title, "test")

    def test_super_create_post(self):
        user = get_user_model().objects.create_superuser(
            username="admin", email="admin@adm.com", password="qwe123QWE!@#"
        )
        post = Post.objects.create(user=user, title="test", description="test desc")
        self.assertTrue(post.approved)
        self.assertFalse(post.is_published)
        self.assertFalse(post.comment_set.count())
        post.is_published = True
        post.refresh_from_db()
        self.assertFalse(post.is_published)
        post.is_published = True
        post.save()
        self.assertTrue(post.approved)
