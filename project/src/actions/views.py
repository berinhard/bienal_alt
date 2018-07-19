from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, reverse
from django.views.generic import ListView

from src.actions.models import Action, QuestionTag


class ListActionsView(ListView):
    context_object_name = 'actions'
    template_name = 'actions/list_actions.html'

    @property
    def search_query(self):
        return self.request.GET.get('q', None)

    @property
    def question_id(self):
        return int(self.request.GET.get('question', 0) or 0)

    @property
    def ordering(self):
        ordering_key = self.request.GET.get('order', 'random').lower()
        if ordering_key == 'time':
            return 'action_date'
        return '?'

    def get_queryset(self, *args, **kwrags):
        if self.search_query:
            qs = Action.objects.search(self.search_query)
        elif self.question_id:
            tag = QuestionTag.objects.get(id=self.question_id)
            qs = tag.actions.all()
        else:
            qs = Action.objects.all()

        return qs.published().order_by(self.ordering)

    def get_context_data(self):
        context = super().get_context_data()
        context['q'] = self.search_query
        context['question_id'] = self.question_id
        return context


def action_detail_view(request, slug):
    action = get_object_or_404(Action.objects.published(), slug=slug)
    prev, next = None, None
    prev_id, next_id = action.id - 1, action.id + 1
    try:
        prev = Action.objects.get(id=prev_id)
    except Action.DoesNotExist:
        pass
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


@login_required
def action_preview_view(request, slug):
    action = get_object_or_404(Action, slug=slug)
    context = {'action': action}
    return render(request, 'actions/action_detail.html', context)
