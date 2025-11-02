from rest_framework import status
from .renderers import UserRenderer
from django.db.models import Q
from rest_framework.response import Response
from mirrorGoal.models import Partnership, Goal
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.serializers import best_buddy_serializer

class View(GenericAPIView):

    serializer_class = best_buddy_serializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        userObj = self.request.user

        partners = Partnership.objects.filter(Q(user_a = userObj) | Q(user_b = userObj), accepted=True)
        best_buddy = {}

        if partners:
            current_partner = partners[0]
            current_partner_goals_count = Goal.objects.filter(user=current_partner, status="Completed").count()

            for partner in partners[1:]:

                partner_goals_count = Goal.objects.filter(user=partner, status="Completed").count()

                if(current_partner_goals_count > partner_goals_count):
                    current_partner = partner
                    current_partner_goals_count = partner_goals_count

        return super().get_queryset()