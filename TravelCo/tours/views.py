from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F

from .models import Tour
from .forms import BookingForm


def list(request):
    tours = Tour.objects.all()
    return render(request, "tour/list.html", {"tours": tours})


def detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == "POST":
        if request.user.is_authenticated:
            booking_form = BookingForm(request.POST, tour=tour)
            if booking_form.is_valid():
                booked = booking_form.save(commit=False)
                booked.tour = tour
                booked.user = request.user
                booked.save()

                # Update the tour's maximum capacity
                Tour.objects.filter(id=tour_id).update(
                    max_capacity=F("max_capacity")
                    - (booked.adults + booked.children + booked.babies)
                )

                return redirect("account:profile")
        else:
            # Store form data in session
            request.session["tour_id"] = tour_id
            request.session["form_data"] = request.POST.dict()
            return redirect("account:login")
    else:
        booking_form = BookingForm(tour=tour)
    return render(request, "tour/detail.html",
                  {"tour": tour, "form": booking_form})
