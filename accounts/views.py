from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import StudentRegistrationForm, StudentProfileUpdateForm
from .models import StudentProfile
from subjects.models import Subject
from admissions.models import AdmissionRequest
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from .forms import LoginForm, ChangeEmailForm
from django.contrib.auth.decorators import login_required
from django.core.signing import TimestampSigner, BadSignature
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model



#change student email
@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.user, request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            signer = TimestampSigner()
            token = signer.sign(f"{request.user.pk}:{new_email}")

            verify_link = request.build_absolute_uri(f'/accounts/verify-email-change/{token}/')

            send_mail(
                subject='Confirm your new email - SchoolMS',
                message=f'Click to confirm your new email:\n\n{verify_link}',
                from_email=None,
                recipient_list=[new_email],
            )
            messages.success(request, 'Verification link sent to your new email!')
            return redirect('change-email')
    else:
        form = ChangeEmailForm(request.user)
    return render(request, 'accounts/change_email.html', {'form': form})

#verify email change
def verify_email_change(request, token):
    signer = TimestampSigner()
    User = get_user_model()
    try:
        value = signer.unsign(token, max_age=86400)
        user_pk, new_email = value.split(':', 1)

        user = User.objects.get(pk=user_pk)
        user.email = new_email
        user.save()
        messages.success(request, 'Email updated successfully! You can now login.')
    except BadSignature:
        messages.error(request, 'Invalid or expired link.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('login')


#LOGIN PAGE
class CustomLoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data["username_or_email"],
            password=form.cleaned_data["password"],
        )

        if user:
            login(self.request, user)
            if user.is_teacher():
                return redirect("teacher-dashboard")
            return redirect("student-dashboard")

        form.add_error(None, "Invalid username/email or password")
        return self.form_invalid(form)


#REGISTER PAGE
class StudentRegisterView(CreateView):
    form_class = StudentRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        
    # PDFs yahan AdmissionRequest mein save honge
        AdmissionRequest.objects.create(
            student=self.object.studentprofile,
            birth_certificate=form.cleaned_data.get('birth_certificate'),
            previous_marksheet=form.cleaned_data.get('previous_marksheet'),
            address_proof=form.cleaned_data.get('address_proof'),
        )
        messages.success(self.request, 'Registration successful! Your admission is under review.')
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('student-dashboard')
        return super().dispatch(request, *args, **kwargs)

#STUDENT DASHVBOARD VIEW
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/student_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_teacher():
            return redirect('teacher-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        student, created = StudentProfile.objects.get_or_create(user=self.request.user)
        
        ctx['student'] = student
        ctx['admission'] = getattr(student, 'admissionrequest', None)
        ctx['enrolled_subjects'] = student.enrolled_subjects.all()
        return ctx

#STUDENT PROFILE UPDATE PAGE
class StudentProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileUpdateForm
    template_name = 'accounts/student_profile.html'
    success_url = reverse_lazy('student-dashboard')

    def get_object(self):
        return self.request.user.studentprofile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

#TEACHER DASHBOARD VIEW
class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/teacher_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_teacher():
            return redirect('student-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        teacher = self.request.user.teacherprofile
        ctx['teacher'] = teacher
        ctx['my_subjects'] = teacher.subjects.prefetch_related('students')
        ctx['total_students'] = sum(s.students.count() for s in teacher.subjects.all())
        return ctx
