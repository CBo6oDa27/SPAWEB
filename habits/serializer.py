from rest_framework.serializers import ModelSerializer

from habits.models import Habit, Reward
from habits.validators import (PeriodicityValidator,
                               PleasantHabitRewardValidator,
                               PleasantHabitValidator,
                               RelatedPleasantHabitValidator,
                               TimeForExecutionValidator)


class HabitSerializer(ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            TimeForExecutionValidator(time_for_execution="time_for_execution"),
            PeriodicityValidator(periodicity="periodicity"),
            PleasantHabitRewardValidator(
                related_pleasant_habit="related_pleasant_habit", reward="reward"
            ),
            PleasantHabitValidator(
                is_pleasant="is_pleasant",
                related_pleasant_habit="related_pleasant_habit",
                reward="reward",
            ),
            RelatedPleasantHabitValidator(),
        ]


class RewardSerializer(ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True)

    class Meta:
        model = Reward
        fields = "__all__"
