from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, id_number, password=None, **extra_fields):
        if not id_number:
            raise ValueError('The ID number must be set')
        # Normalize ID number if needed (strip spaces etc)
        id_number = id_number.strip()
        user = self.model(id_number=id_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(id_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None

    id_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(r'^\d{13}$', 'ID number must be 13 digits')]
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.id_number


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
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='moderate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admins = models.ManyToManyField(User, related_name='assigned_issues', blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.issue_type} - {self.user.id_number}"
