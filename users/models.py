from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    military_experience = models.TextField(blank=True)  # توضیح سابقه نظامی
    nationality = models.CharField(max_length=100, blank=True)
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.PositiveIntegerField(null=True, blank=True)
    
    # نقش: فرض کنیم نقش از قبل مدل شده و مرتبط است
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)

    def can_delete_content(self, content):
        # این متد بررسی می‌کند که آیا کاربر اجازه حذف محتوا را دارد یا نه
        return content.author == self or self.role.name == 'admin'
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # مثلاً admin, user, ...
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
class Mission(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending','Pending'), ('done','Done')], default='pending')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField(null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

