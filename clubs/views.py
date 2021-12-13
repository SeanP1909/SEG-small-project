from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm, LogInForm, UpdateForm, PasswordForm, ClubCreationForm, TournamentForm
from .models import User, Club, Tournament, ClubMember, ClubOfficer

from django.contrib.auth.decorators import login_required

# Create the main page view
def home(request):
    clubs = Club.objects.all()
    return render(request, 'home.html', {"clubs":clubs})


def sign_up(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or ''
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    else:
        next = request.POST.get('next') or ''
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def clubs(request):
    clubs = Club.objects.all()
    return render(request, 'clubs.html', {'clubs': clubs})

@login_required
def profile(request):
    if request.method=='POST':
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def profile_clubs(request):
    return render(request, 'profile_clubs.html')

# Edit password view
@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordForm(data = request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, user.password):
                new_password = form.cleaned_data.get('new_password')
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Password has been updated!")
                return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, "Wrong input! Make sure you get the right password!"
                                                            " A password must contain an uppercase character, a lowercase character, a number"
                                                            " and should match the confirmation.")
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})


# Club page view
def show_club(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
        instance = request.user
        exists_in_club = ClubMember.objects.filter(user=instance.id, club=club.id).prefetch_related('user').prefetch_related('club')
        tournaments = Tournament.objects.filter(club=club.id, finished=False)
        print(tournaments)

    except ObjectDoesNotExist:
        return redirect('home')
    else:
        return render(request, 'show_club.html',
            {'club': club, 'exists_in_club': exists_in_club, 'tournaments': tournaments}
        )

# View for the club creator
@login_required
def club_creator(request):
    if request.method=='POST':
        form = ClubCreationForm(request.POST)
        current_user = request.user
        if form.is_valid():
            name = form.cleaned_data.get('name')
            location = form.cleaned_data.get('location')
            description = form.cleaned_data.get('description')
            club = Club.objects.create(owner=current_user, name=name, location=location, description=description)
            clubmember = ClubMember.objects.create(user=current_user, club=club,role="OWN")
            return redirect('show_club', club.id)
    else:
        form = ClubCreationForm()
    return render(request, 'club_creator.html', {'form': form})

def club_member_list(request, club_id):
    try:
        rU = request.user
        qryClub = Club.objects.get(id=club_id)
        allMembers = ClubMember.objects.filter(club=qryClub.id).prefetch_related('user').prefetch_related('club')
        rU_existsInCLub = ClubMember.objects.filter(user=rU.id,club=qryClub.id).exists()

    except ObjectDoesNotExist:
            return redirect('home')
    else:
        return render(request, 'club_member_list.html', {'members':allMembers, 'club':qryClub, 'exists_in_club':rU_existsInCLub})

def club_member_list_action(request, club_id, userid, action):
    rU = request.user
    qryUser = User.objects.get(id=userid)
    qryClub = Club.objects.get(id=club_id)

    instance_qryUser = qryUser
    instance_qryClub = qryClub

    rU_existsInCLub = ClubMember.objects.filter(user=rU.id,club=instance_qryClub.id)
    rU_isClubOwner = True if instance_qryClub.owner.id == rU.id else False
    qryUser_clubMemberInstance = ClubMember.objects.filter(user=instance_qryUser.id,club=instance_qryClub.id)

    if(rU_existsInCLub and rU_isClubOwner):

        if(action == 'promote'):
            if(qryUser_clubMemberInstance.exists() and qryUser_clubMemberInstance.first().role == 'MEM'):
                promoteOfficer = qryUser_clubMemberInstance.update(role='OFF')

        if(action == 'demote'):
            if(qryUser_clubMemberInstance.exists() and qryUser_clubMemberInstance.first().role == 'OFF'):
                demoteOfficer = qryUser_clubMemberInstance.update(role='MEM')

    allMembers = ClubMember.objects.filter(club=qryClub.id).prefetch_related('user').prefetch_related('club')
    rU_existsInCLub = ClubMember.objects.filter(user=rU.id,club=qryClub.id).exists()
    return render(request, 'club_member_list.html', {'members':allMembers, 'club':qryClub, 'exists_in_club':rU_existsInCLub})

def member_id(request, userid):
    User = get_user_model()
    users = User.objects.filter(id=userid)
    if users:
        return render(request, 'member.html', {'users': users})
    else:
        return redirect('home')

@login_required
def tournaments(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournaments.html', {'tournaments': tournaments})

@login_required
def tournament_organize(request):
    if request.method == 'POST':
        club_id = request.session['club_id']
        club = Club.objects.get(id=club_id)
        organizer = request.user
        form = TournamentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            deadline = form.cleaned_data.get('deadline')
            capacity = form.cleaned_data.get('capacity')
            start = form.cleaned_data.get('start')
            tournament = Tournament.objects.create(
                club = club,
                organizer = organizer,
                name = name,
                description = description,
                capacity = capacity,
                deadline = deadline,
                start = start,
                finished = False
            )
            return redirect('show_club', club_id)
    else:
        form = TournamentForm()
        request.session['club_id'] = request.GET.get('club_id')
    return render(request, 'tournament_edit.html', {'form': form})