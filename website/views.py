from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from django.views.generic import View
from django.db import transaction
from .forms import ProfileForm
from django.contrib import messages




# Create your views here.

@login_required(login_url="login/")
def home(request):
	return render(request, "home.html")

def register_success(request):
    return render(request, "register_success.html")



class UserRegisterForm(View):
    form_class = UserRegisterForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.is_active = False
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "home.html")
            return render(request, "register_success.html")
        return render(request, self.template_name, {'form': form})

@login_required(login_url="login/")
def make_post(request):
    return render(request, "make_post.html")


@login_required(login_url="login/")
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.author)
        if profile_form.is_valid():
            profile_form.save()
            #TODO: send some verification message

            #TODO: should have an else: send some failure message. possibly not needed.
    else:
        profile_form = ProfileForm(instance=request.user.author)
    return render(request, 'profile.html', {
        'profile_form': profile_form
    })
