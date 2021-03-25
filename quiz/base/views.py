from django.db.models.aggregates import Sum
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.utils.timezone import now

from quiz.base.models import Question, Student, StudentAnswer
from quiz.base.forms import StudentForm

def home(request):
    """ Login page """

    if request.method == 'POST':
        student_form = StudentForm(request.POST)

        # User exists
        email = request.POST['email']

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            # User does not exist
            if student_form.is_valid():
                student = student_form.save()
                return redirect('/questions/1')
            else:
                form_context = { 'form': student_form }
                render(request, 'base/home.html', context=form_context)
        else:
            request.session['student_id'] = student.id
            return redirect('/questions/1')

    return render(request, 'base/home.html')

MAX_SCORE = 1000
def questions(request, index):
    """ Questions page """

    try:
        student_id = request.session['student_id']
    except KeyError:
        return redirect('/')
    else:
        try:
            question = Question.objects.filter(available=True).order_by('id')[index - 1]
        except IndexError:
            return redirect('/ranking')
        else:
            context = {'index': index, 'question': question}

            if request.method == 'POST':
                answer_index = int(request.POST['answer_index'])

                if answer_index == question.answer:
                    # Access answer data
                    try:
                        first_answer_date = StudentAnswer.objects.filter(question=question).order_by('answered_in')[0].answered_in
                    except IndexError:
                        StudentAnswer(
                            student_id=student_id,
                            question=question,
                            score=MAX_SCORE
                        ).save()
                    else:
                        difference = now() - first_answer_date
                        diff_seconds = int(difference.total_seconds())
                        score = max(MAX_SCORE - diff_seconds, 10)

                        try:
                            StudentAnswer(
                                student_id=student_id,
                                question=question,
                                score=score
                            ).save()
                        except IntegrityError:
                            return redirect(f'/questions/{index + 1}')

                        return redirect(f'/questions/{index + 1}')

                context['answer_index'] = answer_index
            return render(request, 'base/questions.html', context=context)

def ranking(request):
    """ Ranking page """
    try:
        student_id = request.session['student_id']
    except KeyError:
        return redirect('/')
    else:
        score_dict = StudentAnswer.objects.filter(student=student_id).aggregate(Sum('score'))
        student_score = score_dict['score__sum']
        better_ranked_count = StudentAnswer.objects.values('student').annotate(Sum('score')).filter(score__sum__gt = student_score).count()
        best_ranks = StudentAnswer.objects.values('student', 'student__name').annotate(Sum('score')).order_by('-score__sum')[:5]
        context = {
            'student_score': student_score,
            'student_rank': better_ranked_count + 1,
            'best_ranks': best_ranks
        }
        return render(request, 'base/ranking.html', context)
