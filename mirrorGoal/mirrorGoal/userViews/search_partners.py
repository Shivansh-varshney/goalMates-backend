from .renderers import UserRenderer
from rest_framework.generics import ListAPIView
from django.db.models import Prefetch, Q
from rest_framework.permissions import IsAuthenticated
from mirrorGoal.models import User, Goal, Partnership
from rest_framework.pagination import PageNumberPagination
from mirrorGoal.serializers.partner_suggestions_serializer import Serializer

class View(ListAPIView):
    
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = Serializer

    def get_queryset(self):
        userObj = self.request.user
        query = self.request.query_params.get("query")

        usersList = User.objects.exclude(id=userObj.id).filter(
                    Q(interests__name__icontains=query) |
                    Q(goals__title__icontains=query)
                ).distinct()

        return [
            {
                "id": user.id,
                "name": user.username,
                "location": user.location,
                "bio": user.bio,
                "interests": [tag.name for tag in user.interests.all()],
                "goals": [goal.title.lower() for goal in user.goals.filter(status="Active")],
                "count": 0,
                "requested": False
            }
            for user in usersList
        ]
    
    def get(self, request):

        page = request.query_params.get("page", 1)
        page_size = 12

        try:
            page = int(page)
        except ValueError:
            page = 1
        
        results = self.get_queryset()

        # pagination
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_results = paginator.paginate_queryset(results, request)
        
        serializer = self.get_serializer(paginated_results, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)

        paginated_response.data['status'] = 'success'
        paginated_response.data['message'] = 'results fethced successfully'

        return paginated_response