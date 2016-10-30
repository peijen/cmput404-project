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
        data = {
            "title": "test",
            "author_id": str(author.id),
            "source":"test",
            "origin":"test",
            "description":"test",
            "contentType":"test",
            "content":"test content",
            "categories":"test categories",
            "visibility": "0"
        }
        response = c.post('/service/posts/', data=data, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_can_retrieve_posts_with_http(self):
        Post.objects.create(title="Test123", author_id=author.id)
        Post.objects.create(title="Test345", author_id=author.id)
        Post.objects.create(title="Test567", author_id=author.id)
        response = c.get('/service/posts/')
        list_data = json.loads(response.content.decode('string-escape').strip('"'))
        self.assertEqual(len(list_data), 3)

    def test_can_delete_posts_with_http(self):
        post = Post.objects.create(title="Test123", author_id=author.id)
        response = c.delete('/service/posts/' + str(post.id) +'/')
        self.assertEqual(response.status_code, 200)
        try:
            test = Post.objects.get(pk=post.id)
            self.fail("Should have errored.")
        except:
            pass

    def test_can_retrieve_specific_post_with_http(self):
        post = Post.objects.create(title="Test123", author_id=author.id)
        response = c.get('/service/posts/' + str(post.id) + '/')
        self.assertEqual(response.status_code, 200)
        server_post = json.loads(response.content.decode('string-escape').strip('"'))
        self.assertEqual(str(server_post[0]['pk']), str(post.id))

    def test_can_update_post(self):
        post = Post.objects.create(title="Test123", author_id=author.id)
        response = c.put('/service/posts/' + str(post.id) +'/', {"content":"1"})
        new_post = Post.objects.get(pk=post.id)
        self.assertEqual(new_post.content, "1")

    def test_can_create_with_put(self):
        response = c.put('/service/posts/', json.dumps({"title": "test",
        "author_id": author.id,
        "source":"test",
        "origin":"test",
        "description":"test",
        "contentType":"test",
        "content":"test content",
        "categories":"test categories",
        "visibility": "0"}), content_type="application/json")
        should_exist = Post.objects.get(pk=response['location'].replace('/service/posts/', ''))
