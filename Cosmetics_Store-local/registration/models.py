from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserCustom(AbstractUser):
    avatar = models.ImageField(
        upload_to="images/avatars/",
        default="default/noimage.jpg",
    )

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self) -> str:
        return (
            self.last_name + " " + self.first_name
            if self.last_name and self.first_name
            else "-"
        )
