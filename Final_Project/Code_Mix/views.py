from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum, F, Q, Case, When, IntegerField, ExpressionWrapper, FloatField
from django.db.models.functions import Cast
from django.urls import reverse
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
    
    if not questions.exists():
        return redirect('choose_category')
    
    question_id = id
    if not questions.filter(id=question_id).exists():
        question_easy = questions.first()
    else:
        question_easy = questions.get(id=question_id)
    
    next_questions = questions.filter(id__gt=question_easy.id)
    next_id = next_questions.first().id if next_questions.exists() else questions.first().id
    
    options = Options.objects.filter(question=question_easy)
    context = {
        'question_easy': question_easy,
        'options': options,
        'next_id': next_id,
        'category': category,
    }
    return render(request, 'easy.html', context)

def medium_category(request, id):
    diff_level = 'medium'
    category = request.GET.get('category', None)
    if not category:
        return redirect('choose_category')
    
    questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
    
    if not questions.exists():
        return redirect('choose_category')
    
    question_id = id
    if not questions.filter(id=question_id).exists():
        question_medium = questions.first()
    else:
        question_medium = questions.get(id=question_id)
    
    next_questions = questions.filter(id__gt=question_medium.id)
    next_id = next_questions.first().id if next_questions.exists() else questions.first().id
    
    options = Options.objects.filter(question=question_medium)
    context = {
        'question_medium': question_medium,
        'options': options,
        'next_id': next_id,
        'category': category,
    }
    return render(request, 'medium.html', context)

def hard_category(request, id):
    diff_level = 'hard'
    category = request.GET.get('category', None)
    if not category:
        return redirect('choose_category')
    
    questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
    
    if not questions.exists():
        return redirect('choose_category')
    
    question_id = id
    if not questions.filter(id=question_id).exists():
        question_hard = questions.first()
    else:
        question_hard = questions.get(id=question_id)
    
    next_questions = questions.filter(id__gt=question_hard.id)
    next_id = next_questions.first().id if next_questions.exists() else questions.first().id
    
    options = Options.objects.filter(question=question_hard)
    context = {
        'question_hard': question_hard,
        'options': options,
        'next_id': next_id,
        'category': category,
    }
    return render(request, 'hard.html', context)

def submit_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('selected_option')
        category = request.POST.get('category')
        
        question = get_object_or_404(Questions, id=question_id)
        user_answer = UserAnswer(
            question=question,
            selected_option=selected_option
        )
        user_answer.save()  # This will also set is_correct, category, and difficulty
        
        questions = Questions.objects.filter(
            diff_level=question.diff_level, 
            question_category=question.question_category
        ).order_by('id')
        
        next_questions = questions.filter(id__gt=question.id)
        next_id = next_questions.first().id if next_questions.exists() else questions.first().id
        
        if question.diff_level == 'easy':
            return redirect(f"{reverse('easy_category', args=[next_id])}?category={category}")
        elif question.diff_level == 'medium':
            return redirect(f"{reverse('medium_category', args=[next_id])}?category={category}")
        else:
            return redirect(f"{reverse('hard_category', args=[next_id])}?category={category}")
    
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
