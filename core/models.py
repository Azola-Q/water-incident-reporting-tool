from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id_number = models.CharField(max_length=13, unique=True)
    login_status = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Issue(models.Model):
    ISSUE_TYPES = [
        ('pipe_damage', 'Pipe Damage'),
        ('tap_failure', 'Tap Failure'),
        ('tank_empty', 'Tank Empty'),
        ('illegal_connection', 'Illegal Connection'),
        ('water_leak', 'Water Leak'),
        ('no_water_supply', 'No Water Supply'),
        ('contaminated_water', 'Contaminated Water'),
        ('broken_meter', 'Broken Water Meter'),
        ('low_pressure', 'Low Water Pressure'),
        ('unauthorized_use', 'Unauthorized Water Use'),
        ('sewage_overflow', 'Sewage Overflow'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('received', 'Received'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='moderate')  # New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admins = models.ManyToManyField(User, related_name='assigned_issues', blank=True)

    # Exact location
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.issue_type} - {self.user.username}"
