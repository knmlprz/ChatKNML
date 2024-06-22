import pytest
from django.test import TestCase
from .models import Bot


def create_query():
    return Bot.objects.create(text="example")


class BotModelTests(TestCase):
    @pytest.mark.django_db
    def test_post_method(self):
        create_query()
        assert Bot.objects.filter(text="example").exists(), "Can't create bot object"
