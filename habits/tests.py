from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.habit = Habit.objects.create(
            name="TestHabit", action="TestAction", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Тестирование создания привычки"""
        url = reverse("habits:habit_create")
        data = {"name": "HabitTest", "action": "HabitAction"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)
        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "action": "HabitAction",
                "is_pleasant": False,
                "is_public": False,
                "name": "HabitTest",
                "owner": 1,
                "periodicity": 1,
                "place": None,
                "related_pleasant_habit": None,
                "reward": None,
                "time": None,
                "time_for_execution": 120,
            },
        )

    def test_habit_retrieve(self):
        """Тестирование получения привычки"""
        url = reverse("habits:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], self.habit.name)

    def test_habit_update(self):
        """Тестирование обновления привычки"""
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {"name": "UpdatedHabit"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], "UpdatedHabit")

    def test_habit_list(self):
        """Тестирование вывода списка привычек"""
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "name": self.habit.name,
                    "action": self.habit.action,
                    "place": None,
                    "time": self.habit.time,
                    "is_pleasant": self.habit.is_pleasant,
                    "periodicity": self.habit.periodicity,
                    "time_for_execution": self.habit.time_for_execution,
                    "is_public": self.habit.is_public,
                    "owner": self.user.pk,
                    "related_pleasant_habit": self.habit.related_pleasant_habit,
                    "reward": self.habit.reward,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_destroy(self):
        """Тестирование удаления привычки"""
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_time_for_execution_validator(self):
        """Тестирование создания привычки с временем выполнения большим 120 секунд"""
        url = reverse("habits:habit_create")
        data = {"name": "HabitTest", "action": "HabitAction", "time_for_execution": 150}
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["non_field_errors"],
            ["Время на выполнение не должно быть больше 120 секунд"],
        )
