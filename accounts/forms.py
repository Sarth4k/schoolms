from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile



class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)


#if the user wants to change their email
class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label="New Email")
    current_password = forms.CharField(widget=forms.PasswordInput, label="Current Password")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        password = self.cleaned_data['current_password']
        if not self.user.check_password(password):
            raise forms.ValidationError("Incorrect password")
        return password

    def clean_new_email(self):
        email = self.cleaned_data['new_email']
        User = self.user.__class__
        if User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This email is already in use")
        return email


#STUDENT REGISTRATION FORM
class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=10, required=True)
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    guardian_name = forms.CharField(max_length=100, required=False)
    guardian_phone = forms.CharField(max_length=15, required=False)
    profile_photo = forms.ImageField(required=False)

    # PDF fields — ye AdmissionRequest mein jayenge
    birth_certificate = forms.FileField(required=True)
    previous_marksheet = forms.FileField(required=True)
    address_proof = forms.FileField(required=True)



    # CASE SENSITIVE USERNAME
    def clean_username(self):
        username = self.cleaned_data['username']
        return username.lower()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # StudentProfile mein sirf profile info
            StudentProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                address=self.cleaned_data.get('address', ''),
                guardian_name=self.cleaned_data.get('guardian_name', ''),
                guardian_phone=self.cleaned_data.get('guardian_phone', ''),
                profile_photo=self.cleaned_data.get('profile_photo'),
            )
            # PDFs AdmissionRequest mein jayenge — views.py mein handle hoga
        return user

#STUDENT PROFILE PAGE UPDATE FORM
class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['profile_photo', 'phone', 'date_of_birth', 'address', 'guardian_name', 'guardian_phone']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }