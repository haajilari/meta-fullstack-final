import json
from datetime import datetime

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Booking, Menu


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def book(request):
    return render(request, "book.html")


def reservations(request):
    reservation_records = Booking.objects.all().order_by(
        "reservation_date",
        "reservation_slot",
    )

    booking_json = serializers.serialize(
        "json",
        reservation_records,
    )

    return render(
        request,
        "bookings.html",
        {
            "bookings": booking_json,
            "reservation_records": reservation_records,
        },
    )

@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)

        reservation_slot = int(data["reservation_slot"])

        if reservation_slot < 10 or reservation_slot > 19:
            return HttpResponse(
                '{"error": 2}',
                content_type="application/json",
                status=400,
            )

        exists = Booking.objects.filter(
            reservation_date=data["reservation_date"],
            reservation_slot=reservation_slot,
        ).exists()

        if exists:
            return HttpResponse(
                '{"error": 1}',
                content_type="application/json",
            )

        booking = Booking(
            first_name=data["first_name"],
            reservation_date=data["reservation_date"],
            reservation_slot=reservation_slot,
        )
        booking.save()

    date = request.GET.get(
        "date",
        datetime.today().date(),
    )

    booking_records = Booking.objects.filter(
        reservation_date=date,
    ).order_by("reservation_slot")

    booking_json = serializers.serialize(
        "json",
        booking_records,
    )

    return HttpResponse(
        booking_json,
        content_type="application/json",
    )


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}

    return render(
        request,
        "menu.html",
        {"menu": main_data},
    )


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