from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (
    Partnership, Goal, CheckIn, ProgressHistory, Achievement,
    UserAchievement, NotificationSetting, Notifications, MessageThread, Message, EmailOTP, Activity
)

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = ['is_verified', 'is_staff', 'is_active']

@admin.register(Partnership)
class PartnershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_a', 'user_b', 'accepted', 'created_at']
    list_filter = ['accepted', 'created_at']
    search_fields = ['user_a__email', 'user_b__email']

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'status', 'priority', 'progress', 'current_streak', 'longest_streak', 'completion_date', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['user__email', 'title']

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ['id', 'goal', 'user', 'scheduled_for', 'checked_in_at', 'missed']
    list_filter = ['missed', 'scheduled_for', 'checked_in_at']
    search_fields = ['goal__title', 'user__email']

@admin.register(ProgressHistory)
class ProgressHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'goal', 'recorded_at', 'progress']
    list_filter = ['recorded_at']
    search_fields = ['goal__title']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'achievement', 'goal', 'awarded_at']
    list_filter = ['awarded_at']
    search_fields = ['user__email', 'achievement__name']

@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'enabled']
    list_filter = ['type', 'enabled']
    search_fields = ['user__email', 'type']

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "is_read", "created_at")
    list_filter = ("is_read", "type", "created_at")
    search_fields = ("user__username", "type", "data")
    ordering = ("-created_at",)
    readonly_fields = ("formatted_data",)

    # Optional: make is_read editable directly from the list page
    list_editable = ("is_read",)

    # Optional: pretty print JSON data in admin detail page
    def formatted_data(self, obj):
        import json
        return json.dumps(obj.data, indent=2, ensure_ascii=False)
    formatted_data.short_description = "Data"

    fields = ("user", "type", "is_read", "data", "created_at")

@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_participants']
    search_fields = ['participants__email']

    def get_participants(self, obj):
        return ", ".join([user.email for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

@admin.action(description="Mark as read")
def mark_as_read(modeladmin, request, queryset):
    queryset.update(status="Read")

@admin.action(description="Mark as delivered")
def mark_as_delivered(modeladmin, request, queryset):
    queryset.update(status="Delivered")

@admin.action(description="Mark as sent")
def mark_as_sent(modeladmin, request, queryset):
    queryset.update(status="Sent")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'thread', 'sender', 'sent_at', 'status']
    list_filter = ['sent_at', 'status']
    search_fields = ['sender__email', 'thread__id', 'text']
    actions = [mark_as_read, mark_as_delivered, mark_as_sent]

@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'otp', 'createdAt', 'is_expired']
    list_filter = ['createdAt']
    search_fields = ['email']
    readonly_fields = ['is_expired']

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'activityType', 'time', 'status')
    list_filter = ('activityType', 'status', 'time')
    search_fields = ('user__email', 'title', 'activityType')
    ordering = ('-time',)