from django.views.generic import ListView

from src.actions.models import Action


class ListActionsView(ListView):
    context_object_name = 'actions'
    template_name = 'actions/list_actions.html'

    def get_queryset(self, *args, **kwrags):
        return Action.objects.all()
