from django.test import TestCase, Client
from .models import Author, Comment, Post
import json

# Global setup stuff
c = Client()
author = Author.objects.create()

# Create your tests here.

class TestPosts(TestCase):
    def setUp(self):
        return

    def test_can_create_post_with_db(self):
        test_post = Post.objects.create(title="Test123", author_id=author.id)
        self.assertEqual(test_post.author_id, author.id)

    def test_can_create_post_with_http(self):
        response = c.post('/service/posts/', {'title': 'test', 'author_id': author.id})
        self.assertEqual(response.status_code, 200)

    def test_can_retrieve_posts_with_http(self):
        Post.objects.create(title="Test123", author_id=author.id)
        Post.objects.create(title="Test345", author_id=author.id)
        Post.objects.create(title="Test567", author_id=author.id)
        response = c.get('/service/posts/')
        list_data = json.loads(response.content.decode('string-escape').strip('"'))
        self.assertEqual(len(list_data), 3)
