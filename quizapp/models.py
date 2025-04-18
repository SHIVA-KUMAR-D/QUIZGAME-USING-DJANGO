from django.db import models
from django.contrib.auth.models import User

class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    score = models.IntegerField()
    total = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.language}/{self.topic}: {self.score}/{self.total}'