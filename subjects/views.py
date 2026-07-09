from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Subject, Attendance
from accounts.models import TeacherProfile, StudentProfile

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
    
class SubjectDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'subjects/subject_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        subject = get_object_or_404(Subject, id=self.kwargs['subject_id'])
        ctx['subject'] = subject
        ctx['teachers'] = subject.teachers.all()

        if self.request.user.is_student():
            student = self.request.user.studentprofile
            records = Attendance.objects.filter(
                subject=subject,
                student=student
            ).order_by('-date')

            total = records.count()
            present = records.filter(status='present').count()
            percentage = round((present / total * 100), 1) if total > 0 else 0

            ctx['attendance_records'] = records
            ctx['total'] = total
            ctx['present'] = present
            ctx['percentage'] = percentage

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
    
class TeacherAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'subjects/attendance.html'
    login_url = '/accounts/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher():
            return redirect('student-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        subject = get_object_or_404(Subject, id=self.kwargs['subject_id'])
        date = self.request.GET.get('date') or str(timezone.now().date())  # ← self.request
        students = subject.students.all()

        existing = {
            a.student_id: a.status
            for a in Attendance.objects.filter(subject=subject, date=date)
        }

        ctx['subject'] = subject
        ctx['students'] = students
        ctx['date'] = date
        ctx['existing'] = existing
        return ctx

    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        date = request.POST.get('date')
        teacher = request.user.teacherprofile

        for student in subject.students.all():
            status = request.POST.get(f'status_{student.id}', 'absent')
            Attendance.objects.update_or_create(
                subject=subject,
                student=student,
                date=date,
                defaults={
                    'status': status,
                    'marked_by': teacher,
                }
            )
        messages.success(request, f'Attendance saved for {date}!')
        return redirect(f'/subjects/attendance/{subject_id}/?date={date}')


class StudentAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'subjects/student_attendance.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student():
            return redirect('teacher-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = self.request.user.studentprofile
        enrolled_subjects = student.enrolled_subjects.all()

        attendance_data = []
        for subject in enrolled_subjects:
            records = Attendance.objects.filter(subject=subject, student=student)
            total = records.count()
            present = records.filter(status='present').count()
            percentage = round((present / total * 100), 1) if total > 0 else 0

            attendance_data.append({
                'subject': subject,
                'total': total,
                'present': present,
                'percentage': percentage,
            })

        ctx['attendance_data'] = attendance_data
        return ctx


class StudentAttendanceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'subjects/student_attendance_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student():
            return redirect('teacher-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        subject = get_object_or_404(Subject, id=self.kwargs['subject_id'])
        student = self.request.user.studentprofile

        records = Attendance.objects.filter(
            subject=subject,
            student=student
        ).order_by('-date')

        total = records.count()
        present = records.filter(status='present').count()
        percentage = round((present / total * 100), 1) if total > 0 else 0

        ctx['subject'] = subject
        ctx['records'] = records
        ctx['total'] = total
        ctx['present'] = present
        ctx['percentage'] = percentage
        return ctx
