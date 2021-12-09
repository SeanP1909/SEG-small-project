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
from .forms import SignUpForm, LogInForm, UpdateForm, PasswordForm, ClubCreationForm
from .models import User, Club
from django.contrib.auth.decorators import login_required

# Create the main page view
def home(request):
    return render(request, 'home.html')


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
    except ObjectDoesNotExist:
        return redirect('home')
    else:
        return render(request, 'show_club.html',
            {'club': club,}
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
            return redirect('show_club', club.id)
    else:
        form = ClubCreationForm()
    return render(request, 'club_creator.html', {'form': form})
