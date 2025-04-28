from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum, F, Q, Case, When, IntegerField, ExpressionWrapper, FloatField
from django.db.models.functions import Cast
from .models import Questions, Options, UserAnswer

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

def submit_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('selected_option')
        
        question = get_object_or_404(Questions, id=question_id)
        user_answer = UserAnswer(
            question=question,
            selected_option=selected_option
        )
        user_answer.save()  # This will also set is_correct, category, and difficulty
        
        if question.diff_level == 'easy':
            return redirect('easy_category', id=1)
        elif question.diff_level == 'medium':
            return redirect('medium_category', id=1)
        else:
            return redirect('hard_category', id=1)
    
    return redirect('index')

def show_scores(request):
    category_scores = UserAnswer.objects.values('category').annotate(
        correct_count=Count('id', filter=Q(is_correct=True)),
        total_count=Count('id'),
        percentage=ExpressionWrapper(
            100.0 * Cast(Count('id', filter=Q(is_correct=True)), FloatField()) / Cast(Count('id'), FloatField()),
            output_field=FloatField()
        )
    ).order_by('category')
    
    difficulty_scores = UserAnswer.objects.values('difficulty').annotate(
        correct_count=Count('id', filter=Q(is_correct=True)),
        total_count=Count('id'),
        percentage=ExpressionWrapper(
            100.0 * Cast(Count('id', filter=Q(is_correct=True)), FloatField()) / Cast(Count('id'), FloatField()),
            output_field=FloatField()
        )
    ).order_by('difficulty')
    
    combined_scores = UserAnswer.objects.values('category', 'difficulty').annotate(
        correct_count=Count('id', filter=Q(is_correct=True)),
        total_count=Count('id'),
        percentage=ExpressionWrapper(
            100.0 * Cast(Count('id', filter=Q(is_correct=True)), FloatField()) / Cast(Count('id'), FloatField()),
            output_field=FloatField()
        )
    ).order_by('category', 'difficulty')
    
    context = {
        'category_scores': category_scores,
        'difficulty_scores': difficulty_scores,
        'combined_scores': combined_scores
    }
    
    return render(request, 'scores.html', context)
