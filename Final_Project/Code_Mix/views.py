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
        'q2': q2,
        'options': options,
    }
    return render(request, 'question1.html', context)


def index(request):
    return render(request, 'index.html')

def choose_type(request, rank):
    # Convert rank to lowercase for case-insensitive comparison
    if rank.lower() == 'bronze':
        rank_value = 1
    elif rank.lower() == 'master':
        rank_value = 2
    else:
        rank_value = None
    questions = Questions.objects.filter(rank=rank_value)
    context = {
        'questions': questions,
        'rank': rank,
    }
    return render(request, 'type.html', context)