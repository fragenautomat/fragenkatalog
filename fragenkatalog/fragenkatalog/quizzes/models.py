from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
import re

from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.utils.text import slugify

from fragenkatalog.compilations.models import Compilation
from fragenkatalog.social.models import Like


class Quiz(models.Model):
    """Represents the quizzes that are presented to the user to solve."""

    class Meta:
        ordering = ["created_at", "title"]

    # mandatory fields
    title = models.CharField(max_length=100, help_text="Quiz title")
    description = models.TextField(help_text="Quiz description")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # autogenerated fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # optional fields
    deadline = models.DateTimeField(help_text="Optional date the task is due to", null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    compilation = models.ForeignKey(Compilation, on_delete=models.CASCADE, null=True, blank=True)

    # generic relation fields
    likes = GenericRelation(Like)

    @property
    def is_expired(self):
        """Return True if the task has passed its optional deadline."""
        return self.deadline and timezone.now() > self.deadline

    @property
    def hashtag_set(self):
        return set(relation.hashtag for relation in self.quizhashtagrelation_set.all())

    @property
    def likers(self):
        return set(like.created_by for like in self.likes.all())

    def liked_by(self, user):
        return self.likes.filter(created_by=user).exists()

    def __str__(self):
        return self.title


class HashTag(models.Model):
    title = models.CharField(max_length=100)

    @property
    def quiz_set(self):
        return set(relation.quiz for relation in self.quizhashtagrelation_set.all())

    def __str__(self):
        return self.title


class QuizHashTagRelation(models.Model):
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return "Relation between quiz {} and hashtag {}".format(
            self.quiz,
            self.hashtag
        )


