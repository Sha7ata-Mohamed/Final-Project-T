from django.shortcuts import render, get_object_or_404, redirect
from .models import Questions, Options

def index(request):
    return render(request, 'index.html')

def choose_category(request):
    diff_level = request.GET.get('diff_level', None)
    if diff_level:
        request.session['diff_level'] = diff_level
    return render(request, 'type.html')

def choose_type(request, diff_level):
    default_question_id = 1
    if diff_level == 'easy':
        return redirect('easy_category', id=default_question_id)
    elif diff_level == 'medium':
        return redirect('medium_category', id=default_question_id)
    elif diff_level == 'hard':
        return redirect('hard_category', id=default_question_id)
    
    return render(request, 'type.html')

def easy_category(request, id):
    diff_level = request.session.get('diff_level', 'easy')
    category = request.GET.get('category', None)
    if not category:
        return redirect('choose_category')
    
    questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
    
    question_easy = get_object_or_404(Questions, diff_level=diff_level, question_category=category)
    options = Options.objects.filter(question=question_easy)
    context = {
        'question_easy': question_easy,
        'options': options,
    }
    return render(request, 'easy.html', context)

def medium_category(request, id):
    question_medium = get_object_or_404(Questions, id=id, diff_level='medium')
    options = Options.objects.filter(question_id=question_medium.id)
    context = {
        'question_medium': question_medium,
        'options': options,
    }
    return render(request, 'medium.html', context)

def hard_category(request, id):
    question_hard = get_object_or_404(Questions, id=id, diff_level='hard')
    options = Options.objects.filter(question_id=question_hard.id)
    context = {
        'question_hard': question_hard,
        'options': options,
    }
    return render(request, 'hard.html', context)