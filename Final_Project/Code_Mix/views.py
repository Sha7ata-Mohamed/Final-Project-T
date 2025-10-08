from collections import defaultdict
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.db.models import Count, Q
from .models import Questions, Options, UserAnswer, QuizProgress, UserPerformance
from django.contrib.auth.decorators import login_required


def profile(request):
    user_progress = None
    if request.user.is_authenticated:
        user_progress = QuizProgress.objects.filter(user=request.user).order_by('last_updated')

    # When the user is not authenticated ``request.user`` is an
    # ``AnonymousUser`` instance. Filtering a ForeignKey field with an
    # anonymous user raises ``ValueError`` because Django expects either a
    # concrete ``User`` instance or ``None``. This caused the profile page to
    # fail for anonymous visitors.  To avoid the exception we only query for
    # scores if the user is authenticated; otherwise we return an empty queryset.
    if request.user.is_authenticated:
        user_scores = (
            UserAnswer.objects.filter(user=request.user)
            .values('category', 'difficulty')
            .annotate(
                correct_count=Count('id', filter=Q(is_correct=True)),
                total_count=Count('id'),
                wrong_count=Count('id', filter=Q(is_correct=False)),
            )
            .order_by('category', 'difficulty')
        )
    else:
        user_scores = UserAnswer.objects.none()

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

    if prg and not Questions.objects.filter(
        id=prg.current_question_id,
        diff_level=diff_level,
        question_category=category,
        options__isnull=False,
    ).exists():
        prg = None

    if prg:
        start_id = prg.current_question_id
    else:
        # get first question id for this combo that has options
        qs = Questions.objects.filter(diff_level=diff_level, question_category=category, options__isnull=False).order_by('id')
        first_question = qs.first()
        if not first_question:
            return redirect('choose_category')
        start_id = first_question.id

    base = reverse(f'{diff_level}_category', args=[start_id])
    return redirect(f"{base}?category={category}")


def _category_view(request, id, diff_level, template_name, context_key):
    category = request.GET.get('category')
    if not category:
        return redirect('choose_category')

    # Get questions that have options
    qs = Questions.objects.filter(
        diff_level=diff_level,
        question_category=category,
        options__isnull=False
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

    opt_obj = Options.objects.filter(question=question).first()
    if not opt_obj:
        return redirect('choose_category')

    show_answer     = (request.GET.get('show_answer') == 'True')
    feedback        = request.GET.get('feedback', '')
    is_correct      = (feedback == 'correct')
    selected_option = request.GET.get('selected_option', '').strip()

    raw = opt_obj.answer.strip()
    if raw in ('option_1', 'option_2', 'option_3', 'option_4'):
        correct_text = getattr(opt_obj, raw).strip()
    else:
        # Handle various answer formats
        if raw.lower().startswith('answer:'):
            _, raw = raw.split(':', 1)
            raw = raw.strip()
        elif raw.lower().startswith('correct answer:'):
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

    question = get_object_or_404(
        Questions.objects.select_related('options').filter(options__isnull=False),
        id=q_id,
    )
    try:
        opts = question.options
    except Options.DoesNotExist:
        return redirect('choose_category')

    raw = opts.answer.strip()
    if raw in ('option_1', 'option_2', 'option_3', 'option_4'):
        correct_text = getattr(opts, raw).strip()
    else:
        # Handle various answer formats
        if raw.lower().startswith('answer:'):
            _, raw = raw.split(':', 1)
            raw = raw.strip()
        elif raw.lower().startswith('correct answer:'):
            _, raw = raw.split(':', 1)
            raw = raw.strip()
        correct_text = raw

    # Compare the selected option with the correct answer
    # Handle cases where the answer might include option prefixes like "A) ", "B) ", etc.
    import html

    # Decode HTML entities in both selected and correct answers
    selected_decoded = html.unescape(selected_text).lower().strip()
    correct_decoded = html.unescape(correct_text).lower().strip()

    # If the correct answer doesn't have a prefix but selected does, compare without prefix
    if selected_decoded.startswith(('a)', 'b)', 'c)', 'd)')) and not correct_decoded.startswith(('a)', 'b)', 'c)', 'd)')):
        # Extract just the answer part after the prefix
        selected_decoded = selected_decoded[2:].strip()

    # If the correct answer has a prefix but selected doesn't, compare the answer parts
    if correct_decoded.startswith(('a)', 'b)', 'c)', 'd)')) and not selected_decoded.startswith(('a)', 'b)', 'c)', 'd)')):
        correct_decoded = correct_decoded[2:].strip()

    is_correct = (selected_decoded == correct_decoded)

    # Debug logging for troubleshooting (only when incorrect for debugging)
    if not is_correct:
        print(f"DEBUG: Question ID: {q_id}")
        print(f"DEBUG: Selected: {repr(selected_text)} -> {repr(selected_decoded)}")
        print(f"DEBUG: Correct: {repr(correct_text)} -> {repr(correct_decoded)}")
        print(f"DEBUG: Match: {is_correct}")
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
        question_category=question.question_category,
        options__isnull=False,
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
    if not request.user.is_authenticated:
        return render(request, 'scores.html', {'category_data': []})

    question_totals = (
        Questions.objects
        .filter(options__isnull=False)
        .values('question_category', 'diff_level')
        .annotate(total_questions=Count('id', distinct=True))
    )

    difficulty_order = {'easy': 0, 'medium': 1, 'hard': 2}

    answer_stats = (
        UserAnswer.objects
        .filter(user=request.user)
        .values('category', 'difficulty')
        .annotate(
            correct_count=Count('id', filter=Q(is_correct=True)),
            wrong_count=Count('id', filter=Q(is_correct=False)),
            total_attempts=Count('id'),
        )
    )
    stats_map = {
        (stat['category'], stat['difficulty']): stat
        for stat in answer_stats
    }

    grouped = defaultdict(lambda: {'totals': {'correct': 0, 'wrong': 0, 'total': 0, 'percentage': 0.0}, 'scores': []})

    for record in sorted(
        question_totals,
        key=lambda item: (item['question_category'], difficulty_order.get(item['diff_level'], 99))
    ):
        category = record['question_category']
        difficulty = record['diff_level']
        total_questions = record['total_questions']

        stat = stats_map.get((category, difficulty), {})
        correct = stat.get('correct_count', 0)
        wrong = stat.get('wrong_count', 0)
        effective_correct = min(correct, total_questions)
        remaining_questions = max(total_questions - effective_correct, 0)
        effective_wrong = min(wrong, remaining_questions)

        percentage = (effective_correct / total_questions * 100.0) if total_questions else 0.0

        score_entry = {
            'category': category,
            'difficulty': difficulty,
            'correct_count': correct,
            'wrong_count': wrong,
            'total_count': total_questions,
            'percentage': percentage,
        }

        grouped[category]['scores'].append(score_entry)
        grouped_totals = grouped[category]['totals']
        grouped_totals['correct'] += effective_correct
        grouped_totals['wrong'] += effective_wrong
        grouped_totals['total'] += total_questions

    category_data = []
    for category, data in sorted(grouped.items(), key=lambda item: item[0]):
        data['scores'].sort(key=lambda entry: difficulty_order.get(entry['difficulty'], 99))
        totals = data['totals']
        if totals['total'] > 0:
            totals['percentage'] = (totals['correct'] * 100.0) / totals['total']
        category_data.append({'category': category, 'totals': totals, 'scores': data['scores']})

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
    if request.user.is_authenticated:
        answers = UserAnswer.objects.filter(user=request.user, category=category, difficulty=difficulty)
    else:
        # For anonymous users, we can't track by session in UserAnswer model
        # since UserAnswer doesn't have session_key field
        answers = UserAnswer.objects.none()  # Return empty queryset

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
    if request.user.is_authenticated:
        answers = UserAnswer.objects.filter(user=request.user, category=category, difficulty=difficulty)
    else:
        # For anonymous users, we can't track by session in UserAnswer model
        # since UserAnswer doesn't have session_key field
        answers = UserAnswer.objects.none()  # Return empty queryset

    correct_count = answers.filter(is_correct=True).count()
    wrong_count = answers.filter(is_correct=False).count()
    questions_qs = Questions.objects.filter(
        diff_level=difficulty,
        question_category=category,
        options__isnull=False,
    )
    total_questions = questions_qs.count()
    attempted_count = answers.count()
    denominator = total_questions or attempted_count

    correct_percentage = (correct_count / denominator * 100) if denominator else 0
    wrong_percentage = (wrong_count / denominator * 100) if denominator else 0

    context = {
        'category': category,
        'difficulty': difficulty,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'total_questions': total_questions,
        'questions_attempted': attempted_count,
        'correct_percentage': correct_percentage,
        'wrong_percentage': wrong_percentage,
    }
    return render(request, 'quiz_summary.html', context)
