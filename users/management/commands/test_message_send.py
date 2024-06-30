import os

from django.core.management import BaseCommand

from habits.services import send_telegram_message


class Command(BaseCommand):
    def handle(self, *args, **options):
        chat_id = os.getenv("TEST_CHAT_ID")
        send_telegram_message("привет, это бот", chat_id)
