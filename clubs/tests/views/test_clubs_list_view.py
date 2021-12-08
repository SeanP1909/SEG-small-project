from django.test import TestCase
from clubs.models import Club

class ClubListTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.response = self.client.get('/clubs/', {'clubs':Club.objects.all()})

    def test_url_clubs_existence(self):
        self.assertEqual(self.response.status_code, 200)

    def test_clubs_content_contains_ChessHub(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'ChessHub')
        self.assertTemplateUsed(self.response, 'clubs.html')

    def test_if_clubs_content_contains_chessList_header(self):
        self.assertContains(self.response, 'Clubs list:')

    def test_clubs1_url_does_not_exist_responses_404(self):
        self.assertEqual(self.client.get('/clubs1/').status_code, 404)
