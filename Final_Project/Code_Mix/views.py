from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count,Q, ExpressionWrapper, FloatField
from django.db.models.functions import Cast
from django.urls import reverse
from .models import Questions, Options, UserAnswer

def home(request):
    return render(request, 'home.html')

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
    
    show_answer = request.GET.get('show_answer', False)
    selected_option = request.GET.get('selected_option', None)
    is_correct = request.GET.get('is_correct', None) == 'True'
    
    correct_answer = None
    explanation = None
    if show_answer:
        option = options.first()
        correct_answer = option.answer
        if hasattr(option, 'explanation'):
            explanation = option.explanation
    
    context = {
        'question_easy': question_easy,
        'options': options,
        'next_id': next_id,
        'category': category,
        'show_answer': show_answer,
        'selected_option': selected_option,
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': explanation
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
    
    show_answer = request.GET.get('show_answer', False)
    selected_option = request.GET.get('selected_option', None)
    is_correct = request.GET.get('is_correct', None) == 'True'
    
    correct_answer = None
    explanation = None
    if show_answer:
        option = options.first()
        correct_answer = option.answer
        if hasattr(option, 'explanation'):
            explanation = option.explanation
    
    context = {
        'question_medium': question_medium,
        'options': options,
        'next_id': next_id,
        'category': category,
        'show_answer': show_answer,
        'selected_option': selected_option,
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': explanation
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
    
    show_answer = request.GET.get('show_answer', False)
    selected_option = request.GET.get('selected_option', None)
    is_correct = request.GET.get('is_correct', None) == 'True'
    
    correct_answer = None
    explanation = None
    if show_answer:
        option = options.first()
        correct_answer = option.answer
        if hasattr(option, 'explanation'):
            explanation = option.explanation
    
    context = {
        'question_hard': question_hard,
        'options': options,
        'next_id': next_id,
        'category': category,
        'show_answer': show_answer,
        'selected_option': selected_option,
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': explanation
    }
    return render(request, 'hard.html', context)

def submit_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('selected_option')
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        
        question = get_object_or_404(Questions, id=question_id)
        option = Options.objects.get(question=question)
        is_correct = (selected_option == option.answer)
        
        user_answer = UserAnswer(
            question=question,
            selected_option=selected_option,
            category=category or question.question_category,
            difficulty=difficulty or question.diff_level,
            is_correct=is_correct
        )
        user_answer.save()
        
        questions = Questions.objects.filter(
            diff_level=question.diff_level, 
            question_category=question.question_category
        ).order_by('id')
        
        next_questions = questions.filter(id__gt=question.id)
        next_id = next_questions.first().id if next_questions.exists() else questions.first().id
        
        if difficulty == 'easy':
            return redirect(f"{reverse('easy_category', args=[question_id])}?category={category}&show_answer=True&selected_option={selected_option}&is_correct={is_correct}")
        elif difficulty == 'medium':
            return redirect(f"{reverse('medium_category', args=[question_id])}?category={category}&show_answer=True&selected_option={selected_option}&is_correct={is_correct}")
        else:
            return redirect(f"{reverse('hard_category', args=[question_id])}?category={category}&show_answer=True&selected_option={selected_option}&is_correct={is_correct}")
    
    return redirect('home')

def show_scores(request):
    total_questions = Questions.objects.values('question_category', 'diff_level').annotate(
        question_count=Count('id')
    ).order_by('question_category', 'diff_level')
    
    question_counts = {}
    for item in total_questions:
        key = (item['question_category'], item['diff_level'])
        question_counts[key] = item['question_count']
    
    user_scores = UserAnswer.objects.values('category', 'difficulty').annotate(
        correct_count=Count('id', filter=Q(is_correct=True)),
        answered_count=Count('id'),
        wrong_count=Count('id', filter=Q(is_correct=False))
    ).order_by('category', 'difficulty')
    
    combined_scores = []
    for score in user_scores:
        key = (score['category'], score['difficulty'])
        total_count = question_counts.get(key, 0)
        
        if score['answered_count'] > total_count:
            total_count = score['answered_count']
        
        percentage = 0
        if score['answered_count'] > 0:
            percentage = (score['correct_count'] / score['answered_count']) * 100
            
        combined_scores.append({
            'category': score['category'],
            'difficulty': score['difficulty'],
            'correct_count': score['correct_count'],
            'wrong_count': score['wrong_count'],
            'answered_count': score['answered_count'],
            'total_count': total_count,
            'percentage': percentage
        })
    
    for item in total_questions:
        key = (item['question_category'], item['diff_level'])
        if not any(s['category'] == key[0] and s['difficulty'] == key[1] for s in combined_scores):
            combined_scores.append({
                'category': item['question_category'],
                'difficulty': item['diff_level'],
                'correct_count': 0,
                'wrong_count': 0,
                'answered_count': 0,
                'total_count': item['question_count'],
                'percentage': 0
            })
    
    category_scores = []
    for category in set(item['question_category'] for item in total_questions):
        category_items = [s for s in combined_scores if s['category'] == category]
        total_correct = sum(item['correct_count'] for item in category_items)
        total_wrong = sum(item['wrong_count'] for item in category_items)
        total_answered = sum(item['answered_count'] for item in category_items)
        total_questions_count = sum(item['total_count'] for item in category_items)
        
        percentage = 0
        if total_answered > 0:
            percentage = (total_correct / total_answered) * 100
            
        category_scores.append({
            'category': category,
            'correct_count': total_correct,
            'wrong_count': total_wrong,
            'answered_count': total_answered,
            'total_count': total_questions_count,
            'percentage': percentage
        })
    
    difficulty_scores = []
    for difficulty in set(item['diff_level'] for item in total_questions):
        difficulty_items = [s for s in combined_scores if s['difficulty'] == difficulty]
        total_correct = sum(item['correct_count'] for item in difficulty_items)
        total_wrong = sum(item['wrong_count'] for item in difficulty_items)
        total_answered = sum(item['answered_count'] for item in difficulty_items)
        total_questions_count = sum(item['total_count'] for item in difficulty_items)
        
        percentage = 0
        if total_answered > 0:
            percentage = (total_correct / total_answered) * 100
            
        difficulty_scores.append({
            'difficulty': difficulty,
            'correct_count': total_correct,
            'wrong_count': total_wrong,
            'answered_count': total_answered,
            'total_count': total_questions_count,
            'percentage': percentage
        })
    
    context = {
        'category_scores': category_scores,
        'difficulty_scores': difficulty_scores,
        'combined_scores': combined_scores
    }
    
    return render(request, 'scores.html', context)
