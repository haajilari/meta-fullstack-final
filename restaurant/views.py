import json
from datetime import datetime

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import BookingForm
from .models import Booking, Menu


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def book(request):
    form = BookingForm()
    return render(request, "book.html", {"form": form})


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)

        exists = Booking.objects.filter(
            reservation_date=data["reservation_date"],
            reservation_slot=data["reservation_slot"],
        ).exists()

        if not exists:
            booking = Booking(
                first_name=data["first_name"],
                reservation_date=data["reservation_date"],
                reservation_slot=data["reservation_slot"],
            )
            booking.save()
        else:
            return HttpResponse(
                '{"error": 1}',
                content_type="application/json",
            )

    date = request.GET.get("date", datetime.today().date())
    booking_records = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize("json", booking_records)

    return HttpResponse(
        booking_json,
        content_type="application/json",
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