from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import Optional

class Hobby(models.Model):
    id: int = models.AutoField(primary_key=True)
    name: str = models.CharField(max_length=255, unique=True)

    def save(self, *args: tuple, **kwargs: dict) -> None:
        # Capitalize the first letter of each word in the name
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class CustomUser(AbstractUser):
    name: Optional[str] = models.CharField(max_length=255, null=True)
    email: str = models.EmailField(unique=True)
    date_of_birth: Optional[models.DateField] = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True, related_name="users")

    REQUIRED_FIELDS: list[str] = ['email', 'name', 'date_of_birth']

    def __str__(self) -> str:
        return self.username


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"