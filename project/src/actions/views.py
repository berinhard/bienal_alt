from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from src.actions.models import Action


class ListActionsView(ListView):
    context_object_name = 'actions'
    template_name = 'actions/list_actions.html'

    def get_queryset(self, *args, **kwrags):
        return Action.objects.all()


def action_detail_view(request, slug):
    action = get_object_or_404(Action, slug=slug)
    return render(request, 'actions/action_detail.html', {'action': action})
