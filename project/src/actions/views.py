from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.utils import ErrorList
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView
from django.http import Http404

from src.actions.forms import ContactForm
from src.actions.models import Action, QuestionTag, Contact
from src.actions.recaptcha import validate_captcha


class ListActionsView(ListView):
    context_object_name = 'actions'
    template_name = 'actions/list_actions.html'

    @property
    def search_query(self):
        return self.request.GET.get('q', None)

    @property
    def question_id(self):
        return int(self.request.GET.get('question', 0) or 0)

    def get_queryset(self, *args, **kwrags):
        if self.search_query:
            qs = Action.objects.search(self.search_query)
        else:
            qs = Action.objects.all()

        if self.question_id:
            try:
                self.tag = QuestionTag.objects.get(id=self.question_id)
                qs = self.tag.actions.all()
            except QuestionTag.DoesNotExist:
                pass

        return qs.published()

    def get_context_data(self):
        context = super().get_context_data()
        context['q'] = self.search_query
        context['question_id'] = self.question_id
        if getattr(self, 'tag', None):
            context['question'] = self.tag
        return context


def action_detail_view(request, slug):
    published_actions = Action.objects.published()
    action = get_object_or_404(published_actions, slug=slug)

    action_index = list(published_actions).index(action)
    prev, next = None, None
    prev_id, next_id = action_index - 1, action_index + 1

    if prev_id >= 0:
        prev = published_actions[prev_id]
    try:
        next = published_actions[next_id]
    except IndexError:
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


class AddContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'actions/contact.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if not validate_captcha(self.request.POST):
            errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
            errors.append(_("Erro na validação do Captcha"))
            return self.form_invalid(form)
        return super().form_valid(form)


def action_carousel_html(request, slug):
    action = get_object_or_404(Action, slug=slug)
    if not action.has_carousel:
        raise Http404
    context = {'action': action, 'total': action.carousel.count()}
    return render(request, 'actions/action_carousel.html', context)
