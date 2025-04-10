from django.shortcuts import render, get_object_or_404
from .models import Questions, Options
# Create your views here.
def show_questions(request):
    questions = Questions.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'questions.html', context)


def show_options(request):
    options_instance = get_object_or_404(Options, id=1)
    #ptions = get_object_or_404(Options, question_id=question_id)
    context = {
        'options_instance': options_instance,
        #'options': options,
    }
    return render(request, 'options.html', context)

