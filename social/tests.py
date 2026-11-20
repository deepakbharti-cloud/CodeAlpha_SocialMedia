from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post
class SocialTest(TestCase):
    def test_flow(self):
        a, b = Client(), Client()
        for c, n in ((a, 'alice'), (b, 'bob')):
            c.post('/register/', {'username': n, 'password1': 'Str0ngPass!9', 'password2': 'Str0ngPass!9'})
        b.post('/', {'text': 'hello world'}); p = Post.objects.get()
        a.get('/u/bob/follow/')
        self.assertContains(a.get('/'), 'hello world')
        a.get(f'/like/{p.pk}/'); self.assertEqual(p.likes.count(), 1)
        a.post(f'/comment/{p.pk}/', {'text': 'nice'}); self.assertEqual(p.comments.count(), 1)
        self.assertEqual(User.objects.get(username='bob').followers.count(), 1)
        self.assertEqual(a.get('/u/bob/').status_code, 200)
