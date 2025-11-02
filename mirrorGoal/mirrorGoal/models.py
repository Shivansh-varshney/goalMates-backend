from pyexpat import model
from django.db import models
from datetime import date, timedelta
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import AbstractUser

GOAL_STATUS = {
    'Active': 'Active',
    'Paused': 'Paused',
    'Completed': 'Completed'
}

ACTIVITY_STATUS = {
    'Pending': 'Pending',
    'Completed': 'Completed'
}

GOAL_PRIORITY = {
    'Low': 'Low', 
    'Medium': 'Medium', 
    'High': 'High'
}

MESSAGE_STATUS = [
    ("Sent", "Sent"),
    ("Delivered", "Delivered"),
    ("Read", "Read"),
]

class User(AbstractUser):
    username = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    user_timezone = models.CharField(max_length=100, null=True, blank=True)
    interests = TaggableManager(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Partnership(models.Model):
    user_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_partnerships')
    user_b = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_partnerships')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_a', 'user_b')

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    progress = models.DecimalField(max_digits=5, default=0.00, decimal_places=2)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Active', choices=GOAL_STATUS)
    tags = TaggableManager(blank=True)
    priority = models.CharField(max_length=10, choices=GOAL_PRIORITY)
    completion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
    def calculate_progress(self):
        total_days = (self.completion_date - self.created_at.date()).days
        days_completed = (date.today() - self.created_at.date()).days
        
        if total_days > 0 and days_completed >= 0:
            return round(min((days_completed / total_days) * 100, 100))
        else:
            return 0
    
    def reset_goal(self):

        if self.longest_streak < self.current_streak:
            self.longest_streak = self.current_streak
        
        self.current_streak = 0
        self.progress = 0
        self.save()
    
    def update_progress(self):
        
        if self.longest_streak < self.current_streak:
            self.longest_streak = self.current_streak
        
        self.current_streak += 1
        self.progress = self.calculate_progress()
        self.save()      

class CheckIn(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_for = models.DateTimeField()
    checked_in_at = models.DateTimeField(null=True, blank=True)
    missed = models.BooleanField(default=False)

class Activity(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    activityType = models.CharField(max_length=256)
    time = models.DateTimeField()
    status = models.CharField(max_length=15, default='Pending', choices=ACTIVITY_STATUS)

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.user.email

class ProgressHistory(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE,related_name='history')
    recorded_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField()

    def __str__(self):
        return self.goal.title

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, null=True, blank=True, on_delete=models.SET_NULL)
    awarded_at = models.DateTimeField(auto_now_add=True)

class NotificationSetting(models.Model):

    NOTIFICATION_TYPES = [
        ("Daily Check-in Reminder", "Daily Check-in Reminder"),
        ("Approaching Deadline", "Approaching Deadline"),
        ("Milestone Achievement", "Milestone Achievement"),
        ("Partner Progress Updates", "Partner Progress Updates"),
        ("New Messages", "New Messages"),
        ("Partner Connection Requests", "Partner Connection Requests"),
        ("Product Updates", "Product Updates"),
        ("Tips and Recommendations", "Tips and Recommendations")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'type')  # Ensure one entry per type per user

class Notifications(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=30)
    data = models.JSONField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    class Meta:

        verbose_name_plural = "Notifications"

    def __str__(self):

        return self.user.username

class MessageThread(models.Model):
    participants = models.ManyToManyField(User)

class Message(models.Model):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=MESSAGE_STATUS, default="Sent")

class EmailOTP(models.Model):

    email = models.EmailField()
    otp = models.CharField(max_length=256)
    createdAt = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.createdAt < timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return self.email