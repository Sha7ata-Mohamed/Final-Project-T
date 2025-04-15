from django.shortcuts import render, get_object_or_404
from .models import Questions, Options

def Question_One(request, question_id):
    question = get_object_or_404(Questions, id=question_id)
    options = Options.objects.filter(question_id=question)  # Using 'question_id' for filtering
    context = {
        'question': question,
        'options': options,
    }
    return render(request, 'question1.html', context)

def Question_Two(request, question_id):
    q = get_object_or_404(Questions, id=question_id)
    o = Options.objects.filter(question_id=q)  # Using 'question_id' for filtering
    context = {
        'q': q,
        'o': o,
    }
    return render(request, 'question2.html', context)