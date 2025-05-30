from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


# -------------------------------
# Custom User for Mercenaries
# -------------------------------
class MercenaryUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username, password, **extra_fields)


class MercenaryUser(AbstractUser):
    objects = MercenaryUserManager()

    def __str__(self):
        return self.username


# -------------------------------
# Mercenary Profile
# -------------------------------
class MercenaryProfile(models.Model):
    user = models.OneToOneField(MercenaryUser, on_delete=models.CASCADE, related_name='profile')

    name = models.CharField(max_length=50)
    military_specialty = models.CharField(max_length=50)
    military_rank = models.CharField(max_length=50)
    battalion = models.CharField(max_length=255)
    nationality = models.CharField(max_length=50)

    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(65)])
    height = models.FloatField(validators=[MinValueValidator(150), MaxValueValidator(200)])
    weight = models.FloatField(validators=[MinValueValidator(50), MaxValueValidator(150)])

    image = models.ImageField(upload_to='mercenary_images/', null=True, blank=True)
    about = models.TextField(blank=True)

    approved = models.BooleanField(default=False, verbose_name="تایید شده")

    def __str__(self):
        return self.user.username


# -------------------------------
# Customer Model (ثبت با alias یکتا)
# -------------------------------
class Customer(models.Model):
    alias = models.CharField(max_length=150, unique=True, verbose_name="نام مستعار")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alias


# -------------------------------
# Mission Model (کارت‌های مأموریت)
# -------------------------------
class Mission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='missions')
    assigned_mercenary = models.ForeignKey(MercenaryUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_missions')

    is_customer_approved = models.BooleanField(default=False)
    is_admin_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -------------------------------
# News Cards (برای صفحه اصلی)
# -------------------------------
class NewsCards(models.Model):
    site_name = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField()
    site_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    api_url = models.URLField("https://example.com/api")  # API برای گرفتن خبر زنده
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_name or "NewsCard"

