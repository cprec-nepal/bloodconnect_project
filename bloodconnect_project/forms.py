from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BloodBank, Donor, SOSRequest, BloodStock

class BloodBankRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=False)
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            blood_bank = BloodBank.objects.create(
                user=user,
                username=self.cleaned_data['username'],
                name=self.cleaned_data['name'],
                city=self.cleaned_data['city'],
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                latitude=self.cleaned_data.get('latitude'),
                longitude=self.cleaned_data.get('longitude'),
                is_verified=False
            )
        return blood_bank

class DonorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'blood_group', 'phone', 'city', 'email']

class SOSRequestForm(forms.ModelForm):
    class Meta:
        model = SOSRequest
        fields = ['requester_name', 'blood_group', 'city', 'phone', 'hospital_name', 'address', 'urgency_notes']

class BloodStockUpdateForm(forms.ModelForm):
    class Meta:
        model = BloodStock
        fields = ['quantity', 'price_per_unit', 'is_available']
