from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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
            return redirect(to="/")
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):  # !!!!
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
