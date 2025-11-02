import random
from mirrorGoal.management.factory import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = "Fill fake data so the frontend can get data for better UI development"

    def handle(self, *args, **options):

        interests = [
            "health", "fitness", "productivity", "mindfulness", "meditation", "yoga", "running", "cycling", "swimming", "weightlifting",
            "reading", "writing", "journaling", "photography", "videography", "cooking", "baking", "nutrition", "veganism", "biohacking",
            "travel", "hiking", "camping", "languages", "music", "podcasts", "art", "drawing", "painting", "technology", "coding",
            "machine learning", "AI", "startups", "entrepreneurship", "finance", "investing", "budgeting", "mental health", "therapy", "self-care",
            "sleep optimization", "habit tracking", "goal setting", "time management", "public speaking", "leadership", "volunteering", "sustainability", "gardening", "DIY crafts"
        ]

        previousUser = None
        NUM_USERS = 100
        GOALS_PER_USER = 5

        users = []
        goals = []
        checkins = []
        achievements = []
        user_achievements = []
        partnerShips = []
        messageThreads = []
        messages = []

        print("\nCreating database...\n")

        # print("Creating users\n")
        # for _ in range(NUM_USERS):
        #     user = UserFactory.create()
        #     users.append(user)
        # print("Created users\n")


        # for user in users:
        #     user.interests.set(random.sample(interests, k=5))

        # print("Creating goals\n")
        # for user in users:
        #     for _ in range(GOALS_PER_USER):

        #         goal = GoalFactory.create(user=user)
        #         goals.append(goal)
        # print("Created goals\n")
    

        # print("Creating checkIns for goals\n")
        # for goal in goals:
        #     goal.tags.set(random.sample(interests, k=3))
        #     checkin = CheckInFactory.create(goal=goal)
        #     checkins.append(checkin)
        # print("Created checkIns for goals\n")


        # print("Creating achievements\n")
        # for _ in range(7):
        #     achievement = AchievementFactory.create()
        #     achievements.append(achievement)
        # print("Created achievements\n")

        
        print("Creating user achievements\n")
        for user in users:

            achievements = Achievement.objects.all()
            achievementsListForUser = random.sample(achievements, random.randint(0,4))
            userGoals = Goal.objects.filter(user=user)

            for achievement in achievementsListForUser:
                userAchievement = UserAchievementFactory.create(
                    user=user,
                    achievement=achievement,
                    goal=random.choice(userGoals)
                )

                user_achievements.append(userAchievement)
        print("Created user achievements\n")
    
        
        # print("Creating partnerships for users\n")
        # for _ in range(NUM_USERS):
        #     users = list(User.objects.all())
        #     user1, user2 = random.sample(users, 2)
        #     if not Partnership.objects.filter(user_a=user1, user_b=user2).exists() and not Partnership.objects.filter(user_a=user2, user_b=user1).exists():
        #         partnerShip = PartnershipFactory.create(user_a = user1, user_b=user2)
        #         partnerShips.append(partnerShip)
        # print("Created partnerships for users\n")
    

        # print("Creating chats between the users\n")
        # for partnerShip in partnerShips:

        #     if not partnerShip.accepted:
        #         continue

        #     user_a = partnerShip.user_a
        #     user_b = partnerShip.user_b

        #     thread = MessageThreadFactory(participants=[user_a, user_b])
        #     messageThreads.append(thread)

        #     msg1 = MessageFactory.create(thread = thread, sender = user_a)
        #     msg2 = MessageFactory.create(thread = thread, sender = user_b)
        #     msg3 = MessageFactory.create(thread = thread, sender = user_a)
        #     msg4 = MessageFactory.create(thread = thread, sender = user_b)
        #     msg5 = MessageFactory.create(thread = thread, sender = user_a)
        #     messages.extend([msg1, msg2, msg3, msg4, msg5])
        # print("Created chats between the users\n")