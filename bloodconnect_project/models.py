from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class BloodBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blood_bank')
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

class Donor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

class SOSRequest(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    requester_name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    hospital_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    urgency_notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester_name} - {self.blood_group} ({self.city})"

class BloodStock(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='stocks')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    quantity = models.IntegerField(default=0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['blood_bank', 'blood_group']

    def __str__(self):
        return f"{self.blood_bank.name} - {self.blood_group}: {self.quantity} units"

    @classmethod
    def create_default_stocks(cls, blood_bank):
        """Create default stock entries for all blood groups."""
        for blood_group, _ in cls.BLOOD_GROUPS:
            cls.objects.get_or_create(
                blood_bank=blood_bank,
                blood_group=blood_group,
                defaults={'quantity': 0, 'price_per_unit': 0.00, 'is_available': False}
            )

@receiver(post_save, sender=BloodBank)
def create_blood_stocks(sender, instance, created, **kwargs):
    """Create default blood stocks when a new blood bank is created."""
    if created:
        BloodStock.create_default_stocks(instance)

@receiver(post_save, sender=User)
def create_blood_bank_profile(sender, instance, created, **kwargs):
    """Create blood bank profile when a user is created."""
    if created and hasattr(instance, 'blood_bank'):
        # Profile already created via BloodBankRegistrationForm
        pass
