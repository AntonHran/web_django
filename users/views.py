from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegistrationForm


class RegisterView(View):
    form_class = RegistrationForm
    template_name = "users/signup.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, message=f"Hi {username}! Your account was created successfully.")
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:root_paginate")
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
