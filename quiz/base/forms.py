from django.forms import ModelForm
from quiz.base.models import Student

class StudentForm(ModelForm):
    class  Meta:
        model = Student
        fields = ['name', 'email']
