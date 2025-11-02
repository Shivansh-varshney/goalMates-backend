import factory
from factory import fuzzy
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from mirrorGoal.models import (
    User, Partnership, Goal, CheckIn, Activity,
    ProgressHistory, Achievement, UserAchievement,
    NotificationSetting, MessageThread, Message
)

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    phone = factory.LazyAttribute(lambda _: fake.phone_number()[:15])
    email = factory.LazyAttribute(lambda _: fake.unique.email())
    bio = factory.LazyAttribute(lambda _: fake.text())
    location = factory.LazyAttribute(lambda _: fake.city())
    user_timezone = factory.LazyAttribute(lambda _: fake.timezone())
    is_verified = factory.LazyAttribute(lambda _: fake.boolean())
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    password = factory.LazyFunction(lambda: make_password("testpassword123"))   # password for the test users 
                                                                                # so I can later use these accounts

    @factory.post_generation
    def interests(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for tag in extracted:
            self.interests.add(tag)


class PartnershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Partnership

    user_a = factory.SubFactory(UserFactory)
    user_b = factory.SubFactory(UserFactory)
    accepted = factory.LazyAttribute(lambda _: fake.boolean())
    created_at = factory.LazyFunction(timezone.now)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=4))
    description = factory.LazyAttribute(lambda _: fake.text())
    progress = factory.LazyAttribute(lambda _: round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, max_value=100), 2))
    current_streak = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=10))
    longest_streak = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=20))
    status = fuzzy.FuzzyChoice(['Active', 'Completed', 'Paused'])
    priority = fuzzy.FuzzyChoice(['Low', 'Medium', 'High'])
    completion_date = factory.LazyFunction(lambda: fake.future_date(end_date="+30d"))
    created_at = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for tag in extracted:
            self.tags.add(tag)


class CheckInFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CheckIn

    goal = factory.SubFactory(GoalFactory)
    user = factory.SelfAttribute('goal.user')
    scheduled_for = factory.LazyFunction(lambda: fake.future_datetime())
    checked_in_at = factory.LazyFunction(lambda: fake.date_time_between(start_date='-1d', end_date='now'))
    missed = factory.LazyAttribute(lambda _: fake.boolean())


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    user = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=3))
    activityType = factory.LazyAttribute(lambda _: fake.word())
    time = factory.LazyFunction(timezone.now)
    status = fuzzy.FuzzyChoice(['Pending', 'Completed', 'Skipped'])


class ProgressHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgressHistory

    goal = factory.SubFactory(GoalFactory)
    recorded_at = factory.LazyFunction(timezone.now)
    progress = factory.LazyAttribute(lambda _: round(fake.pyfloat(min_value=0, max_value=100), 2))

class AchievementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Achievement

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())

class UserAchievementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAchievement

    user = factory.SubFactory(UserFactory)
    achievement = factory.SubFactory(AchievementFactory)
    goal = factory.SubFactory(GoalFactory)
    awarded_at = factory.LazyFunction(timezone.now)

class NotificationSettingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NotificationSetting

    user = factory.SubFactory(UserFactory)
    type = fuzzy.FuzzyChoice([choice[0] for choice in NotificationSetting.NOTIFICATION_TYPES])
    enabled = factory.LazyAttribute(lambda _: fake.boolean())


class MessageThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MessageThread

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for user in extracted:
            self.participants.add(user)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    thread = factory.SubFactory(MessageThreadFactory)
    sender = factory.LazyAttribute(lambda _: UserFactory())
    text = factory.LazyAttribute(lambda _: fake.text())
    sent_at = factory.LazyFunction(timezone.now)
    read = factory.LazyAttribute(lambda _: fake.boolean())
