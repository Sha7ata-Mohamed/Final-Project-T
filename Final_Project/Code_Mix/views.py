from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count,Q, ExpressionWrapper, FloatField
from django.db.models.functions import Cast
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Questions, Options, UserAnswer, QuizSession

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user_answers = UserAnswer.objects.filter(user=request.user).order_by('-created_at')
    
    active_sessions = QuizSession.objects.filter(
        user=request.user, 
        is_completed=False,
        is_paused=False
    ).order_by('-last_activity')
    
    paused_sessions = QuizSession.objects.filter(
        user=request.user, 
        is_completed=False,
        is_paused=True
    ).order_by('-last_activity')
    
    completed_sessions = QuizSession.objects.filter(
        user=request.user, 
        is_completed=True
    ).order_by('-end_time')
    
    category_scores = UserAnswer.objects.filter(user=request.user).values('category').annotate(
        correct_count=Count('id', filter=Q(is_correct=True)),
        total_count=Count('id'),
        percentage=ExpressionWrapper(
            100.0 * Cast(Count('id', filter=Q(is_correct=True)), FloatField()) / Cast(Count('id'), FloatField()),
            output_field=FloatField()
        )
    ).order_by('category')
    
    # Calculate scores by difficulty
    difficulty_scores = UserAnswer.objects.filter(user=request.user).values('difficulty').annotate(
        correct_count=Count('id', filter=Q(is_correct=True)),
        total_count=Count('id'),
        percentage=ExpressionWrapper(
            100.0 * Cast(Count('id', filter=Q(is_correct=True)), FloatField()) / Cast(Count('id'), FloatField()),
            output_field=FloatField()
        )
    ).order_by('difficulty')
    
    context = {
        'user_answers': user_answers,
        'category_scores': category_scores,
        'difficulty_scores': difficulty_scores,
        'active_sessions': active_sessions,
        'paused_sessions': paused_sessions,
        'completed_sessions': completed_sessions,
    }
    
    return render(request, 'registration/profile.html', context)

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

@login_required
def easy_category(request, id):
    diff_level = 'easy'
    category = request.GET.get('category', None)
    if not category:
        return redirect('choose_category')
    
    if request.user.is_authenticated:
        paused_session = QuizSession.get_paused_session(request.user, category, diff_level)
        if paused_session and paused_session.current_question:
            messages.info(request, "Resuming your previous session.")
            question_easy = paused_session.current_question
            paused_session.resume_session()
        else:
            active_session = QuizSession.get_active_session(request.user, category, diff_level)
            if not active_session:
                QuizSession.objects.create(
                    user=request.user,
                    category=category,
                    difficulty=diff_level
                )
            
            questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
            if not questions.exists():
                return redirect('choose_category')
            
            question_id = id
            if not questions.filter(id=question_id).exists():
                question_easy = questions.first()
            else:
                question_easy = questions.get(id=question_id)
    else:
        questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
        if not questions.exists():
            return redirect('choose_category')
        
        question_id = id
        if not questions.filter(id=question_id).exists():
            question_easy = questions.first()
        else:
            question_easy = questions.get(id=question_id)
    
    questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
    next_questions = questions.filter(id__gt=question_easy.id)
    next_id = next_questions.first().id if next_questions.exists() else questions.first().id
    
    if request.user.is_authenticated:
        active_session = QuizSession.get_active_session(request.user, category, diff_level)
        if active_session:
            active_session.update_progress(question_easy)
    
    options = Options.objects.filter(question=question_easy)
    context = {
        'question_easy': question_easy,
        'options': options,
        'next_id': next_id,
        'category': category,
        'has_paused_session': request.user.is_authenticated and QuizSession.objects.filter(
            user=request.user, 
            category=category, 
            difficulty=diff_level,
            is_paused=True
        ).exists(),
    }
    return render(request, 'easy.html', context)

@login_required
def medium_category(request, id):
    diff_level = 'medium'
    category = request.GET.get('category', None)
    if not category:
        return redirect('choose_category')
    
    if request.user.is_authenticated:
        paused_session = QuizSession.get_paused_session(request.user, category, diff_level)
        if paused_session and paused_session.current_question:
            messages.info(request, "Resuming your previous session.")
            question_medium = paused_session.current_question
            paused_session.resume_session()
        else:
            active_session = QuizSession.get_active_session(request.user, category, diff_level)
            if not active_session:
                QuizSession.objects.create(
                    user=request.user,
                    category=category,
                    difficulty=diff_level
                )
            
            questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
            if not questions.exists():
                return redirect('choose_category')
            
            question_id = id
            if not questions.filter(id=question_id).exists():
                question_medium = questions.first()
            else:
                question_medium = questions.get(id=question_id)
    else:
        questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
        if not questions.exists():
            return redirect('choose_category')
        
        question_id = id
        if not questions.filter(id=question_id).exists():
            question_medium = questions.first()
        else:
            question_medium = questions.get(id=question_id)
    
    questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
    next_questions = questions.filter(id__gt=question_medium.id)
    next_id = next_questions.first().id if next_questions.exists() else questions.first().id
    
    if request.user.is_authenticated:
        active_session = QuizSession.get_active_session(request.user, category, diff_level)
        if active_session:
            active_session.update_progress(question_medium)
    
    options = Options.objects.filter(question=question_medium)
    context = {
        'question_medium': question_medium,
        'options': options,
        'next_id': next_id,
        'category': category,
        'has_paused_session': request.user.is_authenticated and QuizSession.objects.filter(
            user=request.user, 
            category=category, 
            difficulty=diff_level,
            is_paused=True
        ).exists(),
    }
    return render(request, 'medium.html', context)

@login_required
def hard_category(request, id):
    diff_level = 'hard'
    category = request.GET.get('category', None)
    if not category:
        return redirect('choose_category')
    
    if request.user.is_authenticated:
        paused_session = QuizSession.get_paused_session(request.user, category, diff_level)
        if paused_session and paused_session.current_question:
            messages.info(request, "Resuming your previous session.")
            question_hard = paused_session.current_question
            paused_session.resume_session()
        else:
            active_session = QuizSession.get_active_session(request.user, category, diff_level)
            if not active_session:
                QuizSession.objects.create(
                    user=request.user,
                    category=category,
                    difficulty=diff_level
                )
            
            questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
            if not questions.exists():
                return redirect('choose_category')
            
            question_id = id
            if not questions.filter(id=question_id).exists():
                question_hard = questions.first()
            else:
                question_hard = questions.get(id=question_id)
    else:
        questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
        if not questions.exists():
            return redirect('choose_category')
        
        question_id = id
        if not questions.filter(id=question_id).exists():
            question_hard = questions.first()
        else:
            question_hard = questions.get(id=question_id)
    
    questions = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
    next_questions = questions.filter(id__gt=question_hard.id)
    next_id = next_questions.first().id if next_questions.exists() else questions.first().id
    
    if request.user.is_authenticated:
        active_session = QuizSession.get_active_session(request.user, category, diff_level)
        if active_session:
            active_session.update_progress(question_hard)
    
    options = Options.objects.filter(question=question_hard)
    context = {
        'question_hard': question_hard,
        'options': options,
        'next_id': next_id,
        'category': category,
        'has_paused_session': request.user.is_authenticated and QuizSession.objects.filter(
            user=request.user, 
            category=category, 
            difficulty=diff_level,
            is_paused=True
        ).exists(),
    }
    return render(request, 'hard.html', context)

@login_required
def submit_answer(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('selected_option')
        category = request.POST.get('category')
        
        question = get_object_or_404(Questions, id=question_id)
        user_answer = UserAnswer(
            question=question,
            selected_option=selected_option,
            user=request.user if request.user.is_authenticated else None
        )
        user_answer.save() 
        
        if request.user.is_authenticated:
            active_session = QuizSession.get_active_session(
                request.user, 
                question.question_category, 
                question.diff_level
            )
            if active_session:
                active_session.update_progress(question)
        
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

@login_required
def pause_session(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        
        if not all([question_id, category, difficulty]):
            messages.error(request, "Missing required information to pause session.")
            return redirect('index')
        
        question = get_object_or_404(Questions, id=question_id)
        
        active_session = QuizSession.get_active_session(request.user, category, difficulty)
        if active_session:
            active_session.pause_session(question)
            messages.success(request, "Your progress has been saved. You can resume later.")
        else:
            session = QuizSession.objects.create(
                user=request.user,
                category=category,
                difficulty=difficulty
            )
            session.pause_session(question)
            messages.success(request, "Your progress has been saved. You can resume later.")
        
        return redirect('profile')
    
    return redirect('index')

@login_required
def complete_session(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        
        if not session_id:
            messages.error(request, "Missing session ID.")
            return redirect('profile')
        
        session = get_object_or_404(QuizSession, id=session_id, user=request.user)
        session.complete_session()
        messages.success(request, "Quiz session completed successfully!")
        
        return redirect('profile')
    
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
