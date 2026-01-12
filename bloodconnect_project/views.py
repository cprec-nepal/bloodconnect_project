"""
Views for BloodConnect Project.
"""

from django.shortcuts import render
from django.http import HttpResponse
from .models import BloodBank  # Removed unused Donor import

def homepage(request):
    """Homepage view."""
    return HttpResponse("Welcome to BloodConnect Project!")

def blood_bank_register(request):
    """Blood bank registration page."""
    return HttpResponse("Blood Bank Registration Page")

def user_login(request):
    """User login page."""
    return HttpResponse("User Login Page")

def user_logout(request):
    """User logout page."""
    return HttpResponse("User Logout Page")

def donor_register(request):
    """Donor registration page."""
    return HttpResponse("Donor Registration Page")

def sos_request_create(request):
    """SOS request page."""
    return HttpResponse("SOS Request Page")

def dashboard(request):
    """Dashboard page."""
    return HttpResponse("Dashboard Page")

def map_view(request):
    """Map page."""
    return HttpResponse("Map Page")

def bank_detail(request, bank_id):
    """Bank detail page."""
    return HttpResponse(f"Bank Detail Page for ID {bank_id}")

def api_blood_banks(request):
    """API endpoint: list of blood banks."""
    return HttpResponse("API: List of Blood Banks")
