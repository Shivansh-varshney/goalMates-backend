from django.db.models import Q
from rest_framework import status
from .renderers import UserRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from mirrorGoal.models import User, Partnership
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.serializers.partnerships_serializer import Serializer

class View(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = Serializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        user = self.request.user
        return Partnership.objects.filter(Q(user_a=user) | Q(user_b=user))
    
    def get(self, request):

        all_partnerships = self.get_queryset()
        partners = all_partnerships.filter(accepted=True)
        partners_serializer = self.get_serializer(partners, many=True)

        recieved_invites = all_partnerships.filter(user_b=request.user, accepted=False)
        recieved_invites_serializer = self.get_serializer(recieved_invites, many=True)

        sent_invites = all_partnerships.filter(user_a=request.user, accepted=False)
        sent_invites_serializer = self.get_serializer(sent_invites, many=True)

        return Response({
            'status': 'success',
            'message': 'Partnerships fetched successfully',
            'partners': partners_serializer.data,
            'recieved_invites': recieved_invites_serializer.data,
            'sent_invites': sent_invites_serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        user_id = request.data.get('user_id')
        user_a = request.user
        user_b = get_object_or_404(User, id=user_id)

        partnership = Partnership.objects.create(
            user_a=user_a,
            user_b=user_b,
        )
        serializer = self.get_serializer(partnership)

        return Response({
            'status': 'success',
            'message': 'Invite sent successfully',
            'invite': serializer.data
        }, status=status.HTTP_201_CREATED)

    def patch(self, request):

        invite_id = request.data.get('invite_id')
        partnership = get_object_or_404(Partnership, id=invite_id, user_b=request.user)
        partnership.accepted = True
        partnership.save()

        return Response({
            'status': 'success',
            'message': 'Invite accepted'
        }, status=status.HTTP_200_OK)
        
    def delete(self, request):

        invite_id = request.data.get('invite_id')
        partnership = get_object_or_404(Partnership, id=invite_id)
        partnership.delete()

        return Response({
            'status': 'success',
            'message': 'Invite deleted'
        }, status=status.HTTP_200_OK)
    