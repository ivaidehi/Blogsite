from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from cloudinary.models import CloudinaryField


# Custom Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        if not username:
            raise ValueError("The Username must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


# Validators
def validate_name(value):
    if not re.match(r"^[a-zA-Z]+$", value):
        raise ValidationError("Name can only contain letters.")


# Choices for States
INDIAN_STATES = [
    ("", "Select State"),
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Delhi", "Delhi"),
    ("Jammu and Kashmir", "Jammu and Kashmir"),
    ("Ladakh", "Ladakh"),
]

REGISTER_AS_CHOICES = [
    ("Doctor", "Doctor"),
    ("Patient", "Patient"),
]


# Custom User Model
class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30, validators=[validate_name])
    last_name = models.CharField(max_length=30, validators=[validate_name])
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)

    # Address Fields
    house_no_name = models.CharField(max_length=100, verbose_name="House No. / Name")
    area = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(regex="^\d{6}$", message="Enter a valid 6-digit pincode")
        ],
    )
    city = models.CharField(max_length=100, verbose_name="Town / City")
    state = models.CharField(max_length=100, choices=INDIAN_STATES)

    profile_image = CloudinaryField("image", blank=True, null=True)

    register_as = models.CharField(
        max_length=10,
        choices=REGISTER_AS_CHOICES,
        verbose_name="Registered As",
        default="Patient",
    )

    # Required Fields
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid-19', 'Covid-19'),
        ('Immunization', 'Immunization'),
    ]

    title = models.CharField(max_length=255)
    image = CloudinaryField('image', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary = models.TextField(max_length=300)
    content = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)  # ✅ Add this field
    image_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.title
