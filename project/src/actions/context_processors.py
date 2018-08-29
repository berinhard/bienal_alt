from src.actions.models import Action, QuestionTag


def list_questions(request):
    return {'all_questions': QuestionTag.objects.all()}


def request_language(request):
    return {'LANGUAGE_CODE': request.LANGUAGE_CODE}
