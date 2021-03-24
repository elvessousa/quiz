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
        return str(self.statement)

class Student(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()
    answered_in = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'question'],
                name='unique_answer'
            )
        ]
