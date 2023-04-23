from django.db import models
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse


from . import forms

def signup_page(request):

    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("publications:feed"))
    return render(request, "authentication/signup.html", context={"form": form})