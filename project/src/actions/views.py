from django.shortcuts import get_object_or_404, render, reverse
from django.views.generic import ListView

from src.actions.models import Action


class ListActionsView(ListView):
    context_object_name = 'actions'
    template_name = 'actions/list_actions.html'

    @property
    def search_query(self):
        return self.request.GET.get('q', None)

    def get_queryset(self, *args, **kwrags):
        if self.search_query:
            return Action.objects.search(self.search_query)
        else:
            return Action.objects.all()

    def get_context_data(self):
        context = super().get_context_data()
        context['q'] = self.search_query
        return context


def action_detail_view(request, slug):
    action = get_object_or_404(Action, slug=slug)
    prev, next = None, None
    prev_id, next_id = action.id - 1, action.id + 1
    if prev_id:
        prev = Action.objects.get(id=prev_id)
    try:
        next = Action.objects.get(id=next_id)
    except Action.DoesNotExist:
        pass
    context = {
        'action': action,
        'prev': prev,
        'next': next
    }
    return render(request, 'actions/action_detail.html', context)
