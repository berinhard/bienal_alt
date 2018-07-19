from src.actions.models import Action, QuestionTag


def list_questions(request):
    return {'questions': QuestionTag.objects.values('id', 'title')}
