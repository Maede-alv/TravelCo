from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from .forms import LoginForm, UserRegistrationForm
from tours.models import Booking


# def login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():       
#     else:
#         form = LoginForm()


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect("account:profile")
    else:
        user_form = UserRegistrationForm()

    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def profile(request):
    bookings = Booking.objects.select_related("tour").filter(user=request.user)
    return render(
        request,
        "account/profile.html",
        {"section": "profile", "bookings": list(bookings)},
    )
