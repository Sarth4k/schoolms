from django.shortcuts import redirect
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

from .forms import LoginForm




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


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/student_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_teacher():
            return redirect('teacher-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        # safely fetch karo — crash nahi hoga
        student, created = StudentProfile.objects.get_or_create(user=self.request.user)
        
        ctx['student'] = student
        ctx['admission'] = getattr(student, 'admissionrequest', None)
        ctx['enrolled_subjects'] = student.enrolled_subjects.all()
        return ctx


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
