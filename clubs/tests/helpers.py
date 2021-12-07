from django.urls import reverse
from clubs.models import Club

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url

# Create second club
class CreateClub:
    def _create_other_club(self):
        club = Club.objects.create(
        name = "Chesser",
        owner=self.user,
        location="London",
        description="This is a second chess club."
    )
        return club

class LogInTester:
    def is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
