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