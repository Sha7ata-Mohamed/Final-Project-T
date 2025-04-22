from django.shortcuts import render, get_object_or_404
from .models import Questions, Options

def easy_category(request, diff_level):
    question_easy = get_object_or_404(Questions, diff_level=diff_level)
    options = Options.objects.filter(question_id=question_easy.id)
    context = {
        'question_easy': question_easy,
        'options': options,
    }
    return render(request, 'easy.html', context)

def Question_Two(request, question_id):
    q2 = get_object_or_404(Questions, id=question_id)
    options = Options.objects.filter(question_id= question_id)  
    context = {
        'q2': q2, 
        'options': options,
    }
    return render(request, 'question2.html', context)


def index(request):
    return render(request, 'index.html')

def choose_type(request, diff_level):
    if diff_level == 'easy':
        diff_level = 'easy'
    elif diff_level == 'medium':
        diff_level = 'medium'
    elif diff_level == 'hard':
        diff_level = 'hard'
    else:
        diff_level = None
    questions = Questions.objects.filter(diff_level=diff_level)
    context = {
        'questions': questions,
        'diff_level': diff_level,
    }
    return render(request, 'type.html', context)