from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MercenaryProfile, Customer


class MercenaryRegisterForm(UserCreationForm):
    name = forms.CharField(label="نام")
    military_specialty = forms.CharField(label="تخصص نظامی")
    military_rank = forms.CharField(label="درجه نظامی")
    battalion = forms.CharField(label="گردان")
    nationality = forms.CharField(label="ملیت")
    age = forms.IntegerField(label="سن")
    height = forms.FloatField(label="قد")
    weight = forms.FloatField(label="وزن")
    about = forms.CharField(label="درباره", widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data["name"]
        if commit:
            user.save()
            MercenaryProfile.objects.create(
                user=user,
                name=self.cleaned_data["name"],
                military_specialty=self.cleaned_data["military_specialty"],
                military_rank=self.cleaned_data["military_rank"],
                battalion=self.cleaned_data["battalion"],
                nationality=self.cleaned_data["nationality"],
                age=self.cleaned_data["age"],
                height=self.cleaned_data["height"],
                weight=self.cleaned_data["weight"],
                about=self.cleaned_data["about"],
            )
        return user


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['alias']
        labels = {
            'alias': 'نام مستعار',
        }

    def clean_alias(self):
        alias = self.cleaned_data['alias']
        qs = Customer.objects.filter(alias__iexact=alias)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("این نام مستعار قبلاً ثبت شده است.")
        return alias

class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['alias']

class LoginForm(forms.Form):
    username = forms.CharField(label="نام کاربری")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
