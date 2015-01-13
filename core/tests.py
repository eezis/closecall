import unittest
from django.test import Client
from django.test import TestCase, SimpleTestCase

# from django.test import TestCase

# # Create your tests here.


# class FirstTimeUser(unittest.TestCase):
class FirstTimeUser(SimpleTestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    # all tests need to be prefixes "test_"
    def test_basics(self):
        print "testing"
        response = self.client.get('/about/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        self.assertInHTML('<title>About The Close Call Database</title>',response.content)

    def test_articles(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('An archive of articles and posts',response.content)

        response = self.client.get('/articles/cars-turning-left/')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('The law may stipulate',response.content)

        # test the issue with the G+ addenda to the url
        response = self.client.get('/articles/cars-turning-left/https://plus.google.com/share/')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('The law may stipulate',response.content)







# # to enable csrf testing (should use at amlit)
# # csrf_client = Client(enforce_csrf_checks=True)


# """ payloads https://docs.djangoproject.com/en/1.7/topics/testing/tools/
# c = Client()
# c.get('/customers/details/', {' name': 'fred', 'age': 7})

# /customers/details/?name=fred&age=7

# or

# >>> c = Client()
# >>> c.get('/customers/details/?name=fred&age=7')

# """

# """
# >>> c = Client()
# >>> c.login(username='fred', password='secret')

# # Now you can access a view that's only available to logged-in users.
# """

# class SimpleResponseTest(TestCase):
#     def setUp(self):
#         # Every test needs a client.
#         self.client = Client()

#     def test_details(self):
#         # user not logged in, but can get page
#         response = self.client.get('/')

#         # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, 200)

#         # Check that the rendered context contains 5 customers.
#         self.assertEqual(len(response.context['customers']), 5)


# def test_login():
#     c = Client()
#     c.login(username='fred', password='secret')
#     # c.post('/login/', {'username': 'Oliver-Ezis', 'password': 'testing'})
