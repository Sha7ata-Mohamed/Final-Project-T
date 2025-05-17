from collections import defaultdict
from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse 
from django.utils import timezone 
from django.utils.http import urlencode 
from django.db.models import Count, Q, F, ExpressionWrapper, FloatField 
from .models import Questions, Options, UserAnswer, QuizProgress, UserPerformance 
from django.contrib.auth.decorators import login_required 


def profile(request):
    user_progress = None
    if request.user.is_authenticated:
        user_progress = QuizProgress.objects.filter(user=request.user).order_by('last_updated')

    user_scores = UserAnswer.objects.filter(user=request.user).values('category', 'difficulty').annotate(
        correct_count=Count('id', filter=Q(is_correct=True)),
        total_count=Count('id'),
        wrong_count=Count('id', filter=Q(is_correct=False)),
    ).order_by('category', 'difficulty')

    return render(request, 'profile.html', {
        'user_progress': user_progress,
        'user_scores':   user_scores,
    })


def home(request):
    if request.user.is_authenticated:
        up = QuizProgress.objects.filter(user=request.user).order_by('-last_updated').first()
    else:
        if not request.session.session_key:
            request.session.create()
        up = QuizProgress.objects.filter(session_key=request.session.session_key).order_by('-last_updated').first()
    return render(request, 'home.html', {'user_progress': up})


def choose_category(request):
    diff = request.GET.get('diff_level')
    if diff in ('easy', 'medium', 'hard'):
        request.session['diff_level'] = diff
    diff_level = request.session.get('diff_level', 'easy')

    if request.user.is_authenticated:
        user_progress = QuizProgress.objects.filter(user=request.user).order_by('-last_updated').first()
    else:
        if not request.session.session_key:
            request.session.create()
        user_progress = QuizProgress.objects.filter(session_key=request.session.session_key).order_by('-last_updated').first()

    context = {
        'diff_level': diff_level,
        'user_progress': user_progress,
    }
    return render(request, 'type.html', context)


def choose_type(request, diff_level):
    category = request.GET.get('category')
    if diff_level not in ('easy', 'medium', 'hard') or not category:
        return redirect('choose_category')

    # Determine starting question based on saved progress
    if request.user.is_authenticated:
        prg = QuizProgress.objects.filter(user=request.user, category=category, difficulty=diff_level).first()
    else:
        if not request.session.session_key:
            request.session.create()
        prg = QuizProgress.objects.filter(session_key=request.session.session_key, category=category, difficulty=diff_level).first()

    if prg:
        start_id = prg.current_question_id
    else:
        # get first question id for this combo
        qs = Questions.objects.filter(diff_level=diff_level, question_category=category).order_by('id')
        start_id = qs.first().id if qs.exists() else 1

    base = reverse(f'{diff_level}_category', args=[start_id])
    return redirect(f"{base}?category={category}")


def _category_view(request, id, diff_level, template_name, context_key):
    category = request.GET.get('category')
    if not category:
        return redirect('choose_category')

    qs = Questions.objects.filter(
        diff_level=diff_level,
        question_category=category
    ).order_by('id')
    if not qs.exists():
        return redirect('choose_category')

    try:
        question = qs.get(id=id)
    except Questions.DoesNotExist:
        question = qs.first()

    nxt     = qs.filter(id__gt=question.id).first() or qs.first()
    next_id = nxt.id
    last    = qs.last()
    is_last = (question.id == last.id) if last else False

    opt_obj = get_object_or_404(Options, question=question)

    show_answer     = (request.GET.get('show_answer') == 'True')
    feedback        = request.GET.get('feedback', '')
    is_correct      = (feedback == 'correct')
    selected_option = request.GET.get('selected_option', '').strip()

    raw = opt_obj.answer.strip()
    if raw in ('option_1', 'option_2', 'option_3', 'option_4'):
        correct_text = getattr(opt_obj, raw).strip()
    else:
        if raw.lower().startswith('answer:'):
            _, raw = raw.split(':', 1)
            raw = raw.strip()
        correct_text = raw

    explanation = getattr(opt_obj, 'explanation', '')

    context = {
        context_key:       question,
        'options':         [opt_obj],
        'next_id':         next_id,
        'category':        category,
        'show_answer':     show_answer,
        'feedback':        feedback,
        'is_correct':      is_correct,
        'selected_option': selected_option,
        'correct_answer':  correct_text,
        'explanation':     explanation,
        'is_last':         is_last,
    }
    return render(request, template_name, context)


def easy_category(request, id):
    return _category_view(request, id, 'easy',   'easy.html',   'question_easy')


def medium_category(request, id):
    return _category_view(request, id, 'medium', 'medium.html', 'question_medium')


def hard_category(request, id):
    return _category_view(request, id, 'hard',   'hard.html',   'question_hard')


def submit_answer(request):
    if request.method != 'POST':
        return redirect('home')

    q_id          = request.POST.get('question_id')
    category      = request.POST.get('category', '')
    difficulty    = request.POST.get('difficulty', '')
    selected_text = request.POST.get('selected_option', '').strip()

    question = get_object_or_404(Questions, id=q_id)
    opts     = get_object_or_404(Options, question=question)

    raw = opts.answer.strip()
    if raw in ('option_1', 'option_2', 'option_3', 'option_4'):
        correct_text = getattr(opts, raw).strip()
    else:
        if raw.lower().startswith('answer:'):
            _, raw = raw.split(':', 1)
            raw = raw.strip()
        correct_text = raw

    is_correct = (selected_text.lower() == correct_text.lower())
    feedback   = 'correct' if is_correct else 'incorrect'

    ua = UserAnswer(
        question=question,
        selected_option=selected_text,
        is_correct=is_correct,
        category=category,
        difficulty=difficulty,
    )
    if request.user.is_authenticated:
        ua.user = request.user
    ua.save()

    # Determine if the current question is the last one
    qs = Questions.objects.filter(
        diff_level=question.diff_level,
        question_category=question.question_category
    ).order_by('id')
    last_question = qs.last()
    is_last = (question.id == last_question.id) if last_question else False

    # Update progress and redirect logic
    nxt = qs.filter(id__gt=question.id).first() or qs.first()

    progress_defaults = {'current_question_id': nxt.id, 'last_updated': timezone.now()}
    if request.user.is_authenticated:
        QuizProgress.objects.update_or_create(
            user=request.user,
            category=category,
            difficulty=difficulty,
            defaults=progress_defaults
        )
    else:
        if not request.session.session_key:
            request.session.create()
        QuizProgress.objects.update_or_create(
            session_key=request.session.session_key,
            category=category,
            difficulty=difficulty,
            defaults=progress_defaults
        )

    if is_last:
        return redirect('quiz_summary', category=category, difficulty=difficulty)

    base = reverse(f'{difficulty}_category', args=[question.id])
    params = {
        'category':        category,
        'show_answer':     'True',
        'feedback':        feedback,
        'selected_option': selected_text,
    }
    return redirect(f"{base}?{urlencode(params)}")


def show_scores(request):
    """
    Aggregates UserAnswer by category/difficulty, computing totals and percentages,
    then renders the scores view.
    """
    user_filter = Q(user=request.user) if request.user.is_authenticated else Q()

    # Aggregate per difficulty
    raw_qs = (
        UserAnswer.objects
        .filter(user_filter)
        .values('category', 'difficulty')
        .annotate(
            correct_count=Count('id', filter=Q(is_correct=True)),
            wrong_count=Count('id', filter=Q(is_correct=False)),
            total_count=Count('id')
        )
        .annotate(
            percentage=ExpressionWrapper(
                F('correct_count') * 100.0 / F('total_count'),
                output_field=FloatField()
            )
        )
        .order_by('category', 'difficulty')
    )

    # Organize by category
    temp = defaultdict(lambda: {'totals': {'correct': 0, 'wrong': 0, 'total': 0, 'percentage': 0.0}, 'scores': []})
    for entry in raw_qs:
        cat = entry['category']
        temp[cat]['scores'].append(entry)
        temp[cat]['totals']['correct'] += entry['correct_count']
        temp[cat]['totals']['wrong']   += entry['wrong_count']
        temp[cat]['totals']['total']   += entry['total_count']

    category_data = []
    for cat, data in temp.items():
        totals = data['totals']
        if totals['total'] > 0:
            totals['percentage'] = (totals['correct'] * 100.0) / totals['total']
        category_data.append({'category': cat, 'totals': totals, 'scores': data['scores']})

    return render(request, 'scores.html', {'category_data': category_data})

@login_required
def performance_view(request):
    agg = UserAnswer.objects.filter(user=request.user).aggregate(
        total=Count('id'),
        correct=Count('id', filter=Q(is_correct=True)),
    )
    agg['wrong'] = agg['total'] - agg['correct']

    perf, _ = UserPerformance.objects.get_or_create(user=request.user)
    perf.total_answered = agg['total']
    perf.total_correct  = agg['correct']
    perf.total_wrong    = agg['wrong']
    perf.save()

    return render(request, 'performance.html', {'performance': perf})

def quiz_performance(request, category, difficulty):
    user_filter = Q(user=request.user) if request.user.is_authenticated else Q(session_key=request.session.session_key)
    answers = UserAnswer.objects.filter(user_filter, category=category, difficulty=difficulty)

    correct_count = answers.filter(is_correct=True).count()
    wrong_count = answers.filter(is_correct=False).count()
    total_count = answers.count()
    percentage = (correct_count / total_count * 100) if total_count > 0 else 0

    context = {
        'category': category,
        'difficulty': difficulty,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'total_count': total_count,
        'percentage': percentage,
    }
    return render(request, 'quiz_performance.html', context)

def quiz_summary(request, category, difficulty):
    user_filter = Q(user=request.user) if request.user.is_authenticated else Q(session_key=request.session.session_key)
    answers = UserAnswer.objects.filter(user_filter, category=category, difficulty=difficulty)

    correct_count = answers.filter(is_correct=True).count()
    wrong_count = answers.filter(is_correct=False).count()
    total_questions = 5  # Assuming there are 5 questions in the quiz

    correct_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    wrong_percentage = (wrong_count / total_questions * 100) if total_questions > 0 else 0

    context = {
        'category': category,
        'difficulty': difficulty,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'total_questions': total_questions,
        'correct_percentage': correct_percentage,
        'wrong_percentage': wrong_percentage,
    }
    return render(request, 'quiz_summary.html', context)
    
