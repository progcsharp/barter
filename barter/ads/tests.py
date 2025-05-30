from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal, Category


class AdTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Books')
        self.ad = Ad.objects.create(
            title="Sample Ad",
            description="Sample description",
            category=self.category,
            condition="new",
            user=self.user
        )

    def test_ad_list_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_ad_detail_view(self):
        response = self.client.get(reverse('ad-detail', args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Ad")

    def test_ad_create_requires_login(self):
        response = self.client.get(reverse('ad-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('ad-create'))
        self.assertEqual(response.status_code, 200)

    def test_ad_creation_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('ad-create'), {
            'title': 'New Ad',
            'description': 'Desc',
            'category': self.category.id,
            'image_url': 'http://example.com/image.jpg',
            'condition': 'used',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 2)


class ExchangeProposalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.category = Category.objects.create(name='Electronics')
        self.ad1 = Ad.objects.create(
            title='Ad 1', description='desc', category=self.category,
            condition='used', user=self.user1
        )
        self.ad2 = Ad.objects.create(
            title='Ad 2', description='desc', category=self.category,
            condition='used', user=self.user2
        )

    def test_proposal_create(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('proposal-create', args=[self.ad2.id]), {
            'your-item': self.ad1.id,
            'comment': 'Interested'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        proposal = ExchangeProposal.objects.first()
        self.assertEqual(proposal.comment, 'Interested')

    def test_proposal_access_control(self):
        self.client.login(username='user1', password='pass')
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2)
        response = self.client.post(reverse('proposal-accepted', args=[proposal.id]))
        self.assertEqual(response.status_code, 403)


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'strongPass123',
            'password2': 'strongPass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_logout(self):
        User.objects.create_user(username='testuser', password='pass')
        login_response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'pass'
        })
        self.assertEqual(login_response.status_code, 302)
        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 302)


class FormValidationTestCase(TestCase):
    def test_register_form_invalid_email(self):
        from ads.forms import RegisterForm
        form = RegisterForm(data={
            'username': 'x',
            'email': 'not-an-email',
            'password1': '12345678aA',
            'password2': '12345678aA'
        })
        self.assertFalse(form.is_valid())

    def test_ad_form_valid(self):
        from ads.forms import AdForm
        cat = Category.objects.create(name="Games")
        form = AdForm(data={
            'title': 'Title',
            'description': 'Desc',
            'category': cat.id,
            'image_url': 'http://example.com/image.jpg',
            'condition': 'used',
        })
        self.assertTrue(form.is_valid())
