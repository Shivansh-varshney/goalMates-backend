from rest_framework import status
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Max
from mirrorGoal.models import Goal, Achievement, UserAchievement, Partnership, Activity, CheckIn

class View(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        userObj = request.user

        goalsList = Goal.objects.filter(user=userObj)
        userGoalStreaks = Goal.objects.filter(user=userObj)
        totalAchievements = Achievement.objects.all()
        userAchievementsList = UserAchievement.objects.filter(user=userObj)
        userPartners = Partnership.objects.filter(Q(user_a=userObj) | Q(user_b=userObj))
        checkInsList = CheckIn.objects.filter(user=userObj, checked_in_at=None, missed=False)
        activitiesList = Activity.objects.filter(user=userObj, status="Pending")

        return JsonResponse({
            "status": "success",
            "message": "User stats fetched successfully",
            "stats": {
                "username": userObj.username,
                "total_goals": goalsList.count(),
                "goals_completed": goalsList.filter(status="Completed").count(),
                "active_goals": goalsList.filter(status="Active").count(),
                "paused_goals": goalsList.filter(status="Paused").count(),
                "total_achievements": totalAchievements.count(),
                "user_achievements": userAchievementsList.count(),
                "user_partners": userPartners.count(),
                "check_ins": checkInsList.count(),
                "activities": activitiesList.count(),
                "longest_streak": userGoalStreaks.aggregate(Max('longest_streak'))['longest_streak__max'] or 0,
                "current_streak": userGoalStreaks.aggregate(Max('current_streak'))['current_streak__max'] or 0
            }
        }, status=status.HTTP_200_OK)