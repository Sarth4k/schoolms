from django.views.generic import TemplateView
from subjects.models import Subject
from accounts.models import TeacherProfile, StudentProfile


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['subjects'] = Subject.objects.prefetch_related('teachers__user').all()
        ctx['teachers'] = TeacherProfile.objects.select_related('user').all()
        ctx['stats'] = {
            'students': StudentProfile.objects.count(),
            'teachers': TeacherProfile.objects.count(),
            'subjects': Subject.objects.count(),
        }
        return ctx
