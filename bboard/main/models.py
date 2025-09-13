from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    send_messages = models.BooleanField(
        default=True, verbose_name="Слать оповещения о новых комментариях?"
    )

    class Meta(AbstractUser.Meta):
        pass
