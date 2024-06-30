from rest_framework import serializers


class PleasantHabitRewardValidator:
    """В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей."""

    def __init__(self, related_pleasant_habit, reward):
        self.related_pleasant_habit = related_pleasant_habit
        self.reward = reward

    def __call__(self, value):
        if value.get(self.related_pleasant_habit) and value.get(self.reward):
            raise serializers.ValidationError(
                "Не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей."
            )


class TimeForExecutionValidator:
    """Время выполнения должно быть не больше 120 секунд."""

    def __init__(self, time_for_execution):
        self.time_for_execution = time_for_execution

    def __call__(self, value):
        value = value.get(self.time_for_execution)
        if value and value > 120:
            raise serializers.ValidationError(
                f"Время на выполнение не должно быть больше 120 секунд"
            )


class RelatedPleasantHabitValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки"""

    def __call__(self, habit: dict):
        if related_habit := habit.get("related_nice_habit"):
            if not related_habit.is_nice:
                raise serializers.ValidationError(
                    f"В связанные привычки могут попадать только привычки с признаком приятной привычки"
                )


class PleasantHabitValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки"""

    def __init__(self, is_pleasant, related_pleasant_habit, reward):
        self.is_pleasant = is_pleasant
        self.related_pleasant_habit = related_pleasant_habit
        self.reward = reward

    def __call__(self, value):
        if (
            value.get(self.is_pleasant)
            and value.get(self.related_pleasant_habit)
            or value.get(self.is_pleasant)
            and value.get(self.reward)
        ):
            raise serializers.ValidationError(
                "У приятной привычки не может быть ни вознаграждения, ни связанной привычки"
            )


class PeriodicityValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""

    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, value):
        val = value.get(self.periodicity)
        if val and val > 7:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней"
            )
