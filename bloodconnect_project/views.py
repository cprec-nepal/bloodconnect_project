"""
Views for BloodConnect Project.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import BloodBank, Donor

# You can use templates later, for now simple HttpResponse works

def homepage(request):
    """Homepage view."""
    return HttpResponse("Welcome to BloodConnect Project!")

def blood_bank_register(request):
    """Blood bank registration page."""
    if request.method == "POST":
        # handle form submission later
        return HttpResponse("Blood Bank Registered Successfully!")
    return HttpResponse("Blood Bank Registration Page")

def user_login(request):
    """User login page."""
    return HttpResponse("User Login Page")

def user_logout(request):
    """User logout page."""
    return HttpResponse("User Logout Page")

def donor_register(request):
    """Donor registration page."""
    if request.method == "POST":
        # handle form submission later
        return HttpResponse("Donor Registered Successfully!")
    return HttpResponse("Donor Registration Page")

def sos_request_create(request):
    """SOS request page."""
    if request.method == "POST":
        # handle SOS form submission later
        return HttpResponse("SOS Request Submitted!")
    return HttpResponse("SOS Request Page")

def dashboard(request):
    """Dashboard page showing some data."""
    # Example: count total banks and donors
    total_banks = BloodBank.objects.count()
    total_donors = Donor.objects.count()
    return HttpResponse(f"Dashboard: {total_banks} banks, {total_donors} donors")

def map_view(request):
    """Map page."""
    return HttpResponse("Map Page (to be implemented with Google Maps)")

def bank_detail(request, bank_id):
    """Bank detail page."""
    bank = get_object_or_404(BloodBank, id=bank_id)
    return HttpResponse(f"Bank Detail Page: {bank.name}, Address: {bank.address}")

def api_blood_banks(request):
    """API endpoint: list of blood banks."""
    banks = BloodBank.objects.all()
    data = ", ".join([bank.name for bank in banks])
    return HttpResponse(f"API: {data}")
