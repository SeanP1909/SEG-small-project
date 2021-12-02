from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm

# Create the main page view
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
