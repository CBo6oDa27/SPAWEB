from django.contrib import admin

from habits.models import Habit, Reward
from users.models import User

admin.site.register(User)
admin.site.register(Habit)
admin.site.register(Reward)
