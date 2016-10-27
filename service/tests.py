from django.test import TestCase, Client

c = Client()
response = c.post('/service/author/', {})
response = c.post('/service/posts/', {'title': 'test', 'author_id':1})
print(response)

# Create your tests here.
