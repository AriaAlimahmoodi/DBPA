from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator



class MercenaryUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        username = self.model(username=username, **extra_fields)
        username.set_password(password)
        username.save(using=self._db)
        return username

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class MercenaryUser(AbstractUser):

    objects = MercenaryUserManager()

    def __str__(self):
        return self.username
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

    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")

    def __str__(self):
        return self.user.username

class Mission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class NewsCards(models.Model):
    site_name = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField()
    site_url = models.URLField()
    description = models.TextField(blank=True, null=True)
    api_url = models.URLField("https://example.com/api")  # برای گرفتن خبر زنده
    enabled = models.BooleanField(default=True)  # فعال بودن منبع
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_name or "NewsCard"

class Customer(models.Model):
    alias = models.CharField(max_length=150, unique=True, verbose_name="نام مستعار")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alias

