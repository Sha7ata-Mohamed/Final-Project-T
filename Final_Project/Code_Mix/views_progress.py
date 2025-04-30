from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Questions
from .models_progress import UserProgress

def save_progress(request):
    """
    Save the user's current progress so they can resume later.
    This view doesn't modify any existing code.
    """
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        
        if not all([question_id, category, difficulty]):
            messages.error(request, "Missing required information to save progress")
            return redirect('index')
        
        if request.user.is_authenticated:
            question = get_object_or_404(Questions, id=question_id)
            
            UserProgress.objects.update_or_create(
                user=request.user,
                category=category,
                difficulty=difficulty,
                defaults={'current_question': question}
            )
            
            messages.success(request, "Your progress has been saved. You can resume later.")
            return redirect('index')
        else:
            messages.warning(request, "Please log in to save your progress")
            request.session['temp_progress'] = {
                'question_id': question_id,
                'category': category,
                'difficulty': difficulty
            }
            return redirect('login')  # Redirect to login page
    
    return redirect('index')

@login_required
def resume_progress(request):
    """
    Show the user's saved progress and allow them to resume.
    This view doesn't modify any existing code.
    """
    progress_list = UserProgress.objects.filter(user=request.user)
    
    context = {
        'progress_list': progress_list
    }
    
    return render(request, 'resume_progress.html', context)

@login_required
def load_progress(request, progress_id):
    """
    Load a specific saved progress and redirect to the appropriate question.
    This view doesn't modify any existing code.
    """
    progress = get_object_or_404(UserProgress, id=progress_id, user=request.user)
    
    if progress.difficulty == 'easy':
        return redirect(f"{reverse('easy_category', args=[progress.current_question.id])}?category={progress.category}")
    elif progress.difficulty == 'medium':
        return redirect(f"{reverse('medium_category', args=[progress.current_question.id])}?category={progress.category}")
    else:  # hard
        return redirect(f"{reverse('hard_category', args=[progress.current_question.id])}?category={progress.category}")
