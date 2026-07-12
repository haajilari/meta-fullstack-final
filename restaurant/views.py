from datetime import datetime

from django.contrib import messages
from django.core import serializers
from django.shortcuts import redirect, render

from .forms import BookingForm
from .models import Booking, Menu


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def book(request):
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your reservation was saved successfully.",
            )
            return redirect("bookings")
    else:
        form = BookingForm()

    return render(request, "book.html", {"form": form})


def bookings(request):
    date = request.GET.get("date", datetime.today().date())
    booking_records = Booking.objects.all().order_by(
        "reservation_date",
        "reservation_slot",
    )
    booking_json = serializers.serialize("json", booking_records)

    return render(
        request,
        "bookings.html",
        {
            "bookings": booking_json,
            "reservation_records": booking_records,
            "date": date,
        },
    )
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, "menu.html", {"menu": main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ""

    return render(
        request,
        "menu_item.html",
        {"menu_item": menu_item},
    )