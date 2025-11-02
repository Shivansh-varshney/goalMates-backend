from django.urls import path

from mirrorGoal.userViews import notifications_view
from . import ( verify_otp_view, generate_and_send_otp_view,
                login_view, user_data_view, user_goals_view,
                notification_settings_view, partnership_view,
                user_checkins_view, user_achievement_view,
                progress_history_view, user_stats_view,
                user_activity_view, partner_suggestions_view,
                notifications_view, activity_logs, partner_goals_history,
                message_threads, chat_messages, search_partners)

urlpatterns = [
    path('generate-otp/', generate_and_send_otp_view.View.as_view(), name='verify_otp'),
    path('verify-otp/', verify_otp_view.View.as_view(), name='verify_otp'),
    path('login/', login_view.View.as_view(), name='login_user'),
    path('profile/', user_data_view.View.as_view(), name='user_profile'),
    path('goals/', user_goals_view.View.as_view(), name='user_goals'),
    path('notification_settings/', notification_settings_view.View.as_view(), name='notification_settings/'),
    path('notifications/', notifications_view.View.as_view(), name='notifications'),
    path('partnerships/', partnership_view.View.as_view(), name='partnerships'),
    path('checkins/', user_checkins_view.View.as_view(), name='checkins'),
    path('achievements/', user_achievement_view.View.as_view(), name='achievements'),
    path('goals-with-history/', progress_history_view.View.as_view(), name='goals_history'),
    path('partners-goals-with-history/', partner_goals_history.View.as_view(), name='partners_goals_history'),
    path('user-stats/', user_stats_view.View.as_view(), name='user-stats'),
    path('user-activities/', user_activity_view.View.as_view(), name='user-activities'),
    path('partner-suggestions/', partner_suggestions_view.View.as_view(), name='partner-suggestions'),
    path('activity-logs/', activity_logs.View.as_view(), name='activity_logs'),
    path('message-threads/', message_threads.View.as_view(), name='message_threads'),
    path('chat-messages/', chat_messages.View.as_view(), name='chat_messages'),
    path('search/', search_partners.View.as_view(), name='search_partners')
]