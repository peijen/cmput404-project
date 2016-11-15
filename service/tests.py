from django.test import TestCase, Client
from .models import Author, Comment, Post, User, FriendRequest
import json
import base64

# Global setup stuff
c = Client()

# Create your tests here.
class TestPosts(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='test@test.com', password='user1')
        self.author = Author.objects.create(user_id=self.user.id)
        c.login(username='user1', password='user1')

    def tearDown(self):
        self.user.delete()
        self.author.delete()

    def test_can_create_post_with_db(self):
        test_post = Post.objects.create(title="Test123", author_id=self.author.id)
        self.assertEqual(test_post.author_id, self.author.id)

    def test_can_create_post_with_http(self):
        data = {
            "title": "test",
            "author_id": str(self.author.id),
            "source":"test",
            "origin":"test",
            "description":"test",
            "contentType":"test",
            "content":"test content",
            "categories":"test categories",
            "visibility": "0"
        }
        response = c.post('/service/posts/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_can_retrieve_posts_with_http(self):
        Post.objects.create(title="Test123", author_id=self.author.id)
        Post.objects.create(title="Test345", author_id=self.author.id)
        Post.objects.create(title="Test567", author_id=self.author.id)
        response = c.get('/service/posts/')
        list_data = json.loads(response.content)
        self.assertEqual(len(list_data), 3)

    def test_can_delete_posts_with_http(self):
        post = Post.objects.create(title="Test123", author_id=self.author.id)
        response = c.delete('/service/posts/' + str(post.id) +'/')
        self.assertEqual(response.status_code, 200)
        try:
            test = Post.objects.get(pk=post.id)
            self.fail("Should have errored.")
        except:
            pass

    def test_can_retrieve_specific_post_with_http(self):
        post = Post.objects.create(title="Test123", author_id=self.author.id)
        response = c.get('/service/posts/' + str(post.id) + '/')
        self.assertEqual(response.status_code, 200)
        server_post = json.loads(response.content)
        self.assertEqual(str(server_post['id']), str(post.id))

    def test_can_update_post(self):
        post = Post.objects.create(title="Test123", author_id=self.author.id)
        response = c.put('/service/posts/' + str(post.id) +'/', json.dumps({"content":"1"}))
        new_post = Post.objects.get(pk=post.id)
        self.assertEqual(new_post.content, "1")

    def test_can_create_with_put(self):
        response = c.put('/service/posts/', json.dumps({"title": "test",
        "author_id": self.author.id,
        "source":"test",
        "origin":"test",
        "description":"test",
        "contentType":"test",
        "content":"test content",
        "categories":"test categories",
        "visibility": "0"}), content_type="application/json")
        should_exist = Post.objects.get(pk=response['location'].replace('/service/posts/', ''))

    def test_can_make_friend_requests(self):
        user2 = User.objects.create_user(username='testuser2', email='bebebebe@test.com', password='user2')
        author2 = Author.objects.create(user_id=user2.id)
        response = c.post('/service/friendrequest/', json.dumps({"author_id": str(author2.id)}), content_type="application/json")
        should_exist = FriendRequest.objects.get(pk=response['location'].replace('/service/friendrequest/', ''))

    def test_can_retrieve_pending_friend_requests(self):
        user2 = User.objects.create_user(username='user2', email='test@test.com', password='test')
        user3 = User.objects.create_user(username='user3', email='test@test.com', password='test')
        user4 = User.objects.create_user(username='user4', email='test@test.com', password='test')
        user5 = User.objects.create_user(username='user5', email='test@test.com', password='test')

        author2 = Author.objects.create(user_id=user2.id)
        author3 = Author.objects.create(user_id=user3.id)
        author4 = Author.objects.create(user_id=user4.id)
        author5 = Author.objects.create(user_id=user5.id)

        response = c.post('/service/friendrequest/', json.dumps({"author_id": str(author2.id)}), content_type="application/json")
        response = c.post('/service/friendrequest/', json.dumps({"author_id": str(author3.id)}), content_type="application/json")
        response = c.post('/service/friendrequest/', json.dumps({"author_id": str(author4.id)}), content_type="application/json")
        response = c.post('/service/friendrequest/', json.dumps({"author_id": str(author5.id)}), content_type="application/json")

        response = c.get('/service/friendrequest/')
        content = json.loads(response.content)
        self.assertEqual(len(content), 4)

    def test_also_retrieves_friend_requests_where_is_requestee(self):
        user2 = User.objects.create_user(username='user2', email='test@test.com', password='test')
        user3 = User.objects.create_user(username='user3', email='test@test.com', password='test')
        user4 = User.objects.create_user(username='user4', email='test@test.com', password='test')
        user5 = User.objects.create_user(username='user5', email='test@test.com', password='test')

        author2 = Author.objects.create(user_id=user2.id)
        author3 = Author.objects.create(user_id=user3.id)
        author4 = Author.objects.create(user_id=user4.id)
        author5 = Author.objects.create(user_id=user5.id)

        fr1 = FriendRequest.objects.create(requester=author2, requestee=self.author)
        fr2 = FriendRequest.objects.create(requester=author3, requestee=self.author)
        fr3 = FriendRequest.objects.create(requester=author4, requestee=self.author)
        fr4 = FriendRequest.objects.create(requester=author5, requestee=author2)

        response = c.get('/service/friendrequest/')
        content = json.loads(response.content)
        self.assertEqual(len(content), 3)
        return

    def can_retrieve_list_of_friends(self):

        return
