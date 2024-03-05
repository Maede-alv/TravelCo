from django import forms
from .models import Booking, TourSchedule


class BookingForm(forms.ModelForm):
    tour_schedule = forms.ModelChoiceField(queryset=None, empty_label=None)

    class Meta:
        model = Booking
        fields = ["tour_schedule", "adults", "children", "babies"]

    def __init__(self, *args, **kwargs):
        tour = kwargs.pop("tour")
        super().__init__(*args, **kwargs)
        self.fields["tour_schedule"].queryset = TourSchedule.objects.filter(tour=tour)
