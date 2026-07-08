from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Subject


#LISSTING ALL SUBJECTS ON HOMEPAGE
class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'

    def dispatch(self, request, *args, **kwargs):
        # only approved students can enroll
        if request.user.is_authenticated and request.user.is_student():
            admission = getattr(request.user.studentprofile, 'admissionrequest', None)
            if not admission or admission.status != 'approved':
                messages.warning(request, 'Your admission must be approved before enrolling in subjects.')
                return redirect('student-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Subject.objects.prefetch_related('teachers__user', 'students').all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_student():
            ctx['enrolled_ids'] = list(
                self.request.user.studentprofile.enrolled_subjects.values_list('id', flat=True)
            )
        return ctx

#LISTING ENROLLED SUBJECTS ON STUDENT DASHBOARD
class EnrollView(LoginRequiredMixin, View):
    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        student = request.user.studentprofile
        if student.enrolled_subjects.filter(id=subject_id).exists():
            student.enrolled_subjects.remove(subject)
            messages.info(request, f'Unenrolled from {subject.name}.')
        else:
            student.enrolled_subjects.add(subject)
            messages.success(request, f'Enrolled in {subject.name} successfully!')
        return redirect('subject-list')
