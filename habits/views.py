from django.db.models import Q
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit, Reward
from habits.paginators import ClassesPaginator
from habits.serializer import HabitSerializer, RewardSerializer
from users.permissions import IsOwner


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = ClassesPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = Habit.objects.filter(
            Q(is_public=True) | Q(owner=self.request.user)
        )
        return self.queryset


class HabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitDestroyAPIView(DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitUpdateAPIView(UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class RewardViewSet(ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [IsOwner]
