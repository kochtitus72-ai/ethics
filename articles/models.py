# articles/models.py
import hashlib
import hmac

from django.conf import settings
from django.db import models


def obfuscate_title(title: str) -> str:
    """
    Generate a short obfuscated ID from the article title.
    """
    return hmac.new(
        key=settings.SECRET_KEY.encode(),
        msg=title.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()[:16]


class Person(models.Model):
    """
    Represents a person mentioned in an article.
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    Represents a location mentioned in an article.
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Represents a user-submitted report.
    """

    title = models.CharField(
        max_length=255
    )  # original title (hidden from normal users)
    public_id = models.CharField(
        max_length=16, unique=True, editable=False, null=True, blank=True
    )

    people = models.ManyToManyField(Person, related_name="articles", blank=True)
    location = models.ForeignKey(
        Location,
        related_name="articles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = obfuscate_title(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        # Don't leak the title
        return self.public_id
