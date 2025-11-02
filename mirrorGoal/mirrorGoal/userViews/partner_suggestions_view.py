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

        # Current user's data
        user_interests = set(tag.name.lower() for tag in userObj.interests.all())
        user_goals = Goal.objects.filter(user=userObj)
        user_goal_titles = set(goal.title.lower() for goal in user_goals)

        # --- Exclude existing partnerships ---
        existing_partner_ids = Partnership.objects.filter(
            Q(user_a=userObj) | Q(user_b=userObj)
        ).values_list("user_a", "user_b", flat=False)

        # Flatten + remove self
        existing_partner_ids = set(
            uid for pair in existing_partner_ids for uid in pair if uid != userObj.id
        )

        # Prefetch only active goals for efficiency
        active_goals_prefetch = Prefetch(
            "goals",
            queryset=Goal.objects.filter(status="Active"),
            to_attr="active_goals"
        )

        # Get potential partners excluding current user + existing partners
        exclude_ids = {userObj.id} | existing_partner_ids
        usersList = (
            User.objects.exclude(id__in=exclude_ids)
            .prefetch_related(active_goals_prefetch, "interests")
        )

        partnersList = []

        for user in usersList:
            other_user_goal_titles = [goal.title.lower() for goal in user.active_goals]
            other_user_interests = set(tag.name.lower() for tag in user.interests.all())

            # Check for common goals
            common_titles = [
                title for title in other_user_goal_titles
                if any(user_title in title or title in user_title for user_title in user_goal_titles)
            ]

            # Check for common interests
            has_common_interests = bool(user_interests & other_user_interests)

            if common_titles or has_common_interests:
                partnersList.append({
                    "id": user.id,
                    "name": user.username,
                    "location": user.location,
                    "bio": user.bio,
                    "goals": other_user_goal_titles,
                    "interests": user.interests.all(),
                    "count": len(common_titles),
                    "requested": False 
                })

        if not partnersList:
            fallback_users = User.objects.exclude(id__in=exclude_ids).prefetch_related(
                active_goals_prefetch, "interests"
            )

            for user in fallback_users:
                partnersList.append({
                    "id": user.id,
                    "name": user.username,
                    "location": user.location,
                    "bio": user.bio,
                    "interests": user.interests.all(),
                    "goals": [goal.title.lower() for goal in user.active_goals],
                    "count": 0,
                    "requested": False
                })

        return partnersList

    def get(self, request):

        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size') or PageNumberPagination.page_size

        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        try:
            page_size = int(page_size)
        except ValueError:
            page_size = PageNumberPagination.page_size

        partners = self.get_queryset()

        # Paginate the list manually
        paginator = PageNumberPagination()
        paginator.page_size = page_size  # Or use settings
        paginated_partners = paginator.paginate_queryset(partners, request)

        serializer = self.get_serializer(paginated_partners, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)

        # Modify the original paginated response and inject additional metadata
        paginated_response.data['status'] = "success"
        paginated_response.data['message'] = "Partners fetched successfully"
        paginated_response.data['suggestions'] = paginated_response.data.pop('results')

        return paginated_response
