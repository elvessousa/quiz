from django.db import models

# Create your models here.

class Question(models.Model):
    statement = models.TextField()
    options = models.JSONField()
    available = models.BooleanField(default=False)
    answer = models.IntegerField(choices=[
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D')
    ])

    def __str__(self):
        return self.statement

