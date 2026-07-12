from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        widgets = {
            "reservation_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "reservation_slot": forms.Select(),
        }