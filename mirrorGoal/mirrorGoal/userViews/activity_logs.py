from rest_framework import status
from .renderers import UserRenderer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from mirrorGoal.models import Activity, Partnership
from mirrorGoal.serializers.activity_logs_serializer import Serializer

class View(ListAPIView):

    serializer_class = Serializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        userObj = self.request.user
        partnerships = Partnership.objects.filter(Q(user_a = userObj) | Q(user_b=userObj), accepted=True)

        partner_ids = []
        for p in partnerships:
            if p.user_a == userObj:
                partner_ids.append(p.user_b.id)
            else:
                partner_ids.append(p.user_a.id)

        # Include the current user + all partners
        return Activity.objects.filter(
            user__id__in=[userObj.id] + partner_ids,
            status="Completed"
        ).order_by("-time")
    
    def get(self, request):

        activities = self.get_queryset()
        serializer = self.get_serializer(activities, many=True, context={"request": request})

        return Response({
            "stauts": "message",
            "message": "Activity logs fetched successfully",
            "activities": serializer.data
        }, status=status.HTTP_200_OK)