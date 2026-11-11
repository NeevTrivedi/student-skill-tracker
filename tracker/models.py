from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CATEGORY_CHOICES = [
    ('Programming', 'Programming'),
    ('Web Development', 'Web Development'),
    ('Communication', 'Communication'),
    ('Technical Skills', 'Technical Skills'),
    ('Management', 'Management'),
    ('Creativity', 'Creativity'),
    ('Other Skills', 'Other Skills'),
]

PROFICIENCY_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]

GOAL_TYPE_CHOICES = [
    ('Weekly', 'Weekly Goal'),
    ('Monthly', 'Monthly Goal'),
]

YEAR_CHOICES = [
    ('1st Year', '1st Year'),
    ('2nd Year', '2nd Year'),
    ('3rd Year', '3rd Year'),
    ('4th Year', '4th Year'),
    ('Postgraduate', 'Postgraduate'),
]

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    college = models.CharField(max_length=255, blank=True)
    course = models.CharField(max_length=150, blank=True)
    year_of_study = models.CharField(max_length=20, choices=YEAR_CHOICES, default='1st Year')
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Automatic signal to create/update StudentProfile on User creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='Beginner')
    progress_percentage = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    target_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class LearningGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES, default='Weekly')
    target_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']