from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import BloodBank, Donor, SOSRequest, BloodStock
from .forms import BloodBankRegistrationForm, DonorRegistrationForm, SOSRequestForm, BloodStockUpdateForm
from .google_sheets import (
    sync_blood_bank_to_sheets,
    sync_donor_to_sheets,
    sync_sos_request_to_sheets,
    sync_blood_stock_to_sheets
)
import logging

logger = logging.getLogger(__name__)

def homepage(request):
    """Homepage view with search functionality."""
    city = request.GET.get('city', '')
    blood_group = request.GET.get('blood_group', '')
    
    blood_banks = BloodBank.objects.filter(is_verified=True)
    
    if city:
        blood_banks = blood_banks.filter(city__icontains=city)
    
    if blood_group:
        blood_banks = blood_banks.filter(stocks__blood_group=blood_group, stocks__is_available=True)
    
    sos_requests = SOSRequest.objects.filter(is_active=True).order_by('-created_at')[:10]
    
    context = {
        'blood_banks': blood_banks.distinct(),
        'sos_requests': sos_requests,
        'city': city,
        'blood_group': blood_group,
    }
    
    return render(request, 'bloodconnect/home.html', context)

def blood_bank_register(request):
    """Blood bank registration view."""
    if request.method == 'POST':
        form = BloodBankRegistrationForm(request.POST)
        if form.is_valid():
            blood_bank = form.save()
            
            # Sync to Google Sheets (non-blocking)
            try:
                sync_blood_bank_to_sheets(blood_bank)
            except Exception as e:
                logger.error(f"Failed to sync blood bank to Google Sheets: {e}")
            
            messages.success(
                request,
                f'Registration successful! Your account "{blood_bank.username}" has been created. '
                'Please wait for admin verification before your blood bank appears on the platform. '
                'You can login after admin approval.'
            )
            return redirect('bloodconnect:login')
    else:
        form = BloodBankRegistrationForm()
    
    return render(request, 'bloodconnect/register.html', {'form': form})

def user_login(request):
    """User login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                blood_bank = user.blood_bank
                if blood_bank.is_verified:
                    login(request, user)
                    messages.success(request, f'Welcome back, {blood_bank.name}!')
                    return redirect('bloodconnect:dashboard')
                else:
                    messages.error(request, 'Your account is pending verification by admin. Please wait for approval.')
            except BloodBank.DoesNotExist:
                messages.error(request, 'Blood bank profile not found. Please contact admin.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'bloodconnect/login.html')

@login_required
def user_logout(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('bloodconnect:homepage')

def donor_register(request):
    """Donor registration view."""
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            donor = form.save()
            
            # Sync to Google Sheets (non-blocking)
            try:
                sync_donor_to_sheets(donor)
            except Exception as e:
                logger.error(f"Failed to sync donor to Google Sheets: {e}")
            
            messages.success(
                request,
                f'Thank you, {donor.name}! Your registration as a donor is complete. '
                'Blood banks may contact you when your blood group is needed.'
            )
            return redirect('bloodconnect:homepage')
    else:
        form = DonorRegistrationForm()
    
    return render(request, 'bloodconnect/donor_register.html', {'form': form})

def sos_request_create(request):
    """Create urgent SOS blood request."""
    if request.method == 'POST':
        form = SOSRequestForm(request.POST)
        if form.is_valid():
            sos_request = form.save()
            
            # Sync to Google Sheets (non-blocking)
            try:
                sync_sos_request_to_sheets(sos_request)
            except Exception as e:
                logger.error(f"Failed to sync SOS request to Google Sheets: {e}")
            
            messages.success(
                request,
                f'Urgent blood request created successfully! '
                f'Your request for {sos_request.blood_group} blood in {sos_request.city} is now active.'
            )
            return redirect('bloodconnect:homepage')
    else:
        form = SOSRequestForm()
    
    return render(request, 'bloodconnect/sos_request.html', {'form': form})

@login_required
def dashboard(request):
    """Bank dashboard view."""
    try:
        blood_bank = request.user.blood_bank
    except BloodBank.DoesNotExist:
        messages.error(request, 'Blood bank profile not found. Please contact admin.')
        return redirect('bloodconnect:homepage')
    
    # Ensure all blood group stocks exist
    BloodStock.create_default_stocks(blood_bank)
    
    stocks = BloodStock.objects.filter(blood_bank=blood_bank).order_by('blood_group')
    
    if request.method == 'POST':
        updated_count = 0
        for stock in stocks:
            form = BloodStockUpdateForm(request.POST, prefix=f'stock_{stock.id}', instance=stock)
            if form.is_valid():
                stock = form.save()
                
                # Sync to Google Sheets (non-blocking)
                try:
                    sync_blood_stock_to_sheets(stock)
                except Exception as e:
                    logger.error(f"Failed to sync blood stock to Google Sheets: {e}")
                
                updated_count += 1
        
        if updated_count > 0:
            messages.success(request, f'Successfully updated {updated_count} stock entries.')
        else:
            messages.warning(request, 'No stock entries were updated.')
        
        return redirect('bloodconnect:dashboard')
    
    stock_forms = []
    for stock in stocks:
        form = BloodStockUpdateForm(prefix=f'stock_{stock.id}', instance=stock)
        stock_forms.append({
            'form': form,
            'stock': stock,
            'blood_group': stock.blood_group,
        })
    
    context = {
        'blood_bank': blood_bank,
        'stock_forms': stock_forms,
    }
    
    return render(request, 'bloodconnect/dashboard.html', context)

def map_view(request):
    """Live Google Maps view."""
    bank_id = request.GET.get('bank_id')
    city = request.GET.get('city', '')
    blood_group = request.GET.get('blood_group', '')
    
    banks = BloodBank.objects.filter(is_verified=True)
    
    if city:
        banks = banks.filter(city__icontains=city)
    
    if bank_id:
        banks = banks.filter(id=bank_id)
    
    context = {
        'blood_banks': banks,
        'bank_id': bank_id,
        'city': city,
        'blood_group': blood_group,
    }
    
    return render(request, 'bloodconnect/map.html', context)

def bank_detail(request, bank_id):
    """Blood bank detail view."""
    bank = get_object_or_404(BloodBank, id=bank_id, is_verified=True)
    stocks = BloodStock.objects.filter(blood_bank=bank)
    
    context = {
        'bank': bank,
        'stocks': stocks,
    }
    
    return render(request, 'bloodconnect/bank_detail.html', context)

def api_blood_banks(request):
    """JSON API for blood bank locations."""
    banks = BloodBank.objects.filter(is_verified=True).values(
        'id', 'name', 'city', 'address', 'phone', 'email', 'latitude', 'longitude'
    )
    return JsonResponse(list(banks), safe=False)
