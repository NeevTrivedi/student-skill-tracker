from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Skill, LearningGoal, ActivityLog
from .forms import UserRegisterForm, UserUpdateForm, StudentProfileForm, SkillForm, LearningGoalForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            ActivityLog.objects.create(user=user, action_text="Registered account on Skill Tracker.")
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def dashboard_view(request):
    user_skills = Skill.objects.filter(user=request.user)
    total_skills = user_skills.count()
    completed_skills = user_skills.filter(progress_percentage=100).count()
    in_progress_skills = user_skills.filter(progress_percentage__lt=100).count()
    avg_progress = user_skills.aggregate(Avg('progress_percentage'))['progress_percentage__avg'] or 0

    recent_activities = ActivityLog.objects.filter(user=request.user)[:5]
    pending_goals = LearningGoal.objects.filter(user=request.user, is_completed=False)[:3]

    context = {
        'total_skills': total_skills,
        'completed_skills': completed_skills,
        'in_progress_skills': in_progress_skills,
        'avg_progress': round(avg_progress, 1),
        'recent_activities': recent_activities,
        'pending_goals': pending_goals,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def skills_list_view(request):
    skills = Skill.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'tracker/skills.html', {'skills': skills})

@login_required
def skill_create_view(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            ActivityLog.objects.create(user=request.user, action_text=f"Added new skill: {skill.name}")
            messages.success(request, f"Skill '{skill.name}' added successfully!")
            return redirect('skills_list')
    else:
        form = SkillForm()
    return render(request, 'tracker/skill_form.html', {'form': form, 'title': 'Add New Skill'})

@login_required
def skill_edit_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            ActivityLog.objects.create(user=request.user, action_text=f"Updated skill: {skill.name}")
            messages.success(request, f"Skill '{skill.name}' updated!")
            return redirect('skills_list')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'tracker/skill_form.html', {'form': form, 'title': 'Edit Skill'})

@login_required
def skill_delete_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        name = skill.name
        skill.delete()
        ActivityLog.objects.create(user=request.user, action_text=f"Deleted skill: {name}")
        messages.success(request, f"Skill '{name}' deleted.")
        return redirect('skills_list')
    return render(request, 'tracker/skill_confirm_delete.html', {'skill': skill})

@login_required
def goals_view(request):
    if request.method == 'POST':
        form = LearningGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            ActivityLog.objects.create(user=request.user, action_text=f"Created goal: {goal.title}")
            messages.success(request, "Learning goal created successfully.")
            return redirect('goals')
    else:
        form = LearningGoalForm()

    pending_goals = LearningGoal.objects.filter(user=request.user, is_completed=False).order_by('target_date')
    completed_goals = LearningGoal.objects.filter(user=request.user, is_completed=True).order_by('-target_date')

    context = {
        'form': form,
        'pending_goals': pending_goals,
        'completed_goals': completed_goals
    }
    return render(request, 'tracker/goals.html', context)

@login_required
def toggle_goal_view(request, pk):
    goal = get_object_or_404(LearningGoal, pk=pk, user=request.user)
    goal.is_completed = not goal.is_completed
    goal.save()
    status_text = "completed" if goal.is_completed else "marked pending"
    ActivityLog.objects.create(user=request.user, action_text=f"Goal '{goal.title}' {status_text}.")
    return redirect('goals')

@login_required
def delete_goal_view(request, pk):
    goal = get_object_or_404(LearningGoal, pk=pk, user=request.user)
    goal.delete()
    messages.success(request, "Goal removed.")
    return redirect('goals')

@login_required
def analytics_view(request):
    user_skills = Skill.objects.filter(user=request.user)
    category_counts = user_skills.values('category').annotate(count=Count('category'))

    cat_labels = [c['category'] for c in category_counts]
    cat_data = [c['count'] for c in category_counts]

    # Proficiency level counts
    prof_counts = user_skills.values('proficiency').annotate(count=Count('proficiency'))
    prof_dict = {p['proficiency']: p['count'] for p in prof_counts}
    prof_labels = ['Beginner', 'Intermediate', 'Advanced']
    prof_data = [prof_dict.get(label, 0) for label in prof_labels]

    context = {
        'cat_labels': cat_labels,
        'cat_data': cat_data,
        'prof_labels': prof_labels,
        'prof_data': prof_data,
        'total_skills': user_skills.count(),
        'completed_skills': user_skills.filter(progress_percentage=100).count(),
        'goals_completed': LearningGoal.objects.filter(user=request.user, is_completed=True).count(),
        'goals_pending': LearningGoal.objects.filter(user=request.user, is_completed=False).count(),
    }
    return render(request, 'tracker/analytics.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentProfileForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            ActivityLog.objects.create(user=request.user, action_text="Updated student profile information.")
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentProfileForm(instance=request.user.profile)

    return render(request, 'tracker/profile.html', {'u_form': u_form, 'p_form': p_form})