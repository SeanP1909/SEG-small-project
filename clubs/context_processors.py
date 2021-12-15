from .models import ClubMember, Club

def get_associated_clubs_list(request):
    club_list = []
    current_user = request.user
    if current_user.is_authenticated:

        for member in ClubMember.objects.filter(user = current_user).select_related('club'):
            associated_club = Club.objects.get(id = member.club.id)
            club_list.append(associated_club)

    return {'club_list': club_list}
