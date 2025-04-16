from django.shortcuts import render, get_object_or_404
from .models import Questions, Options

def Question_One(request, question_id):
    q1 = get_object_or_404(Questions, id=question_id)
    options = Options.objects.filter(question_id=q1)  # Using 'question_id' for filtering
    context = {
        'q1': q1,
        'options': options,
    }
    return render(request, 'question1.html', context)

def Question_Two(request, question_id):
    q2 = get_object_or_404(Questions, id=question_id)
    options = Options.objects.filter(question_id=q2)  # Using 'question_id' for filtering
    context = {
        'q': q2,
        'o': options,
    }
    return render(request, 'question1.html', context)


def index(request):
    return render(request, 'index.html')

def type(request, type):
    questions = Questions.objects.filter(rank=type)
    context = {
        'questions': questions,
        'type': type,
    }
    return render(request, 'question1.html', context)