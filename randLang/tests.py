
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse

from . import views
# Create your tests here.
class UrlPageTests(SimpleTestCase):

    #Test to make sure home page gives a 302, redirecting to show_letters
    def test_showletters_name_url(self):
        response = self.client.get(reverse('randLang:show_letters'))
        self.assertEquals(response.status_code,302)

    def test_showletters_uses_correct_template(self):
        response = self.client.get(reverse('randLang:show_letters'),follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_letters.html')

    def test_randLang_showletters_status_code(self):
        response = self.client.get('/randLang/show_letters')
        self.assertEquals(response.status_code,302)

    def test_accounts_login_status_code(self):
        response = self.client.get('/accounts/login')
        self.assertEquals(response.status_code,301)

    def test_accounts_login_name_url(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code,200)

    def test_accounts_logout_status_code(self):
        response = self.client.get('/accounts/logout')
        self.assertEquals(response.status_code,301)

    def test_showlang_status_code(self):
        response = self.client.get(reverse('randLang:show_lang'))
        self.assertEquals(response.status_code,302)

'''
TODO add a class that tests the existence of urls once logged in
     add a class that tests the generation of alphabet and Syllables
     add a class that tests the creation of the database model
     add a class that tests the showlang view
     add a class testing registration - get to do some tdd!!
     add a class testing login 
'''
