from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Reward(models.Model):
    """Вознагражение, которое используется в модели привычек"""

    name = models.CharField(verbose_name="Название вознаграждения")
    owner = models.ForeignKey(
        User, verbose_name="создатель", on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"


class Habit(models.Model):
    """Привычка"""

    owner = models.ForeignKey(
        User, verbose_name="владелец", on_delete=models.CASCADE, **NULLABLE
    )
    name = models.CharField(
        verbose_name="Наименование", help_text="Введите наименование привычки"
    )
    place = models.TextField(
        verbose_name="место",
        help_text="Введите место, в котором необходимо выполнять привычку",
        **NULLABLE,
    )
    time = models.TimeField(
        verbose_name="время",
        help_text="Укажите время, когда необходимо выполнять привычку.",
        **NULLABLE,
    )
    action = models.TextField(
        verbose_name="Действие",
        help_text="Введите действие, которое представляет собой привычка.",
    )
    is_pleasant = models.BooleanField(
        default=False, verbose_name="признак приятной привычки"
    )
    related_pleasant_habit = models.ForeignKey(
        "self", verbose_name="связанная привычка", on_delete=models.SET_NULL, **NULLABLE
    )
    periodicity = models.IntegerField(default=1)
    reward = models.ForeignKey(
        Reward, verbose_name="вознаграждение", on_delete=models.SET_NULL, **NULLABLE
    )
    time_for_execution = models.IntegerField(
        default=120, verbose_name="Время на выполнение"
    )
    is_public = models.BooleanField(default=True, verbose_name="Признак публичности")

    send_date = models.DateField(
        auto_now_add=True, verbose_name="дата отправки", **NULLABLE
    )

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
