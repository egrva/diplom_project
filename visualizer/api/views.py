from decimal import Decimal

from django.contrib.auth import authenticate, login
from django.db.models import Q, Avg, Max, Min
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from api.models import Students, StudentStatistic, Marks, Likes, Messages


def student_analyze(request, pk):
    query = StudentStatistic.objects.get(student=pk)
    student_name = str('{second_name} {first_name} {group}').format(second_name=query.student.second_name,
                                                                    first_name=query.student.first_name,
                                                                    group=query.student.group)
    most_popular_time = query.most_popular_time
    likes_count = query.likes_count
    avg_score = query.avg_score
    student_messages_count = query.student_messages_count
    decanat_messages_count = query.decanat_messages_count
    disciplines_labels, disciplines_student_scores, total_scorers, marks = get_student_disciplines(query.student)
    avg_negative_decanat = return_if_not_none(query.avg_negative_decanat, 0)
    avg_negative_student = return_if_not_none(query.avg_negative_student, 0)
    avg_neutral_student = return_if_not_none(query.avg_neutral_student, 0)
    avg_neutral_decanat = return_if_not_none(query.avg_neutral_decanat, 0)
    avg_skip_decanat = return_if_not_none(query.avg_skip_decanat, 0)
    avg_skip_student = return_if_not_none(query.avg_skip_student, 0)
    avg_positive_decanat = return_if_not_none(query.avg_positive_decanat, 0)
    avg_positive_student = return_if_not_none(query.avg_positive_student, 0)
    avg_speech_decanat = return_if_not_none(query.avg_speech_decanat, 0)
    avg_speech_student = return_if_not_none(query.avg_speech_student, 0)

    return render(request, 'analyze_student.html', {
        'student_name': student_name,
        'most_popular_time': most_popular_time,
        'likes_count': likes_count,
        'avg_score': avg_score,
        'student_messages_count': student_messages_count,
        'decanat_messages_count': decanat_messages_count,
        'disciplines_labels': disciplines_labels,
        'disciplines_student_scores': disciplines_student_scores,
        'total_scorers': total_scorers,
        'marks': marks,
        'avg_negative_decanat': avg_negative_decanat,
        'avg_negative_student': avg_negative_student,
        'avg_neutral_student': avg_neutral_student,
        'avg_neutral_decanat': avg_neutral_decanat,
        'avg_skip_decanat': avg_skip_decanat,
        'avg_skip_student': avg_skip_student,
        'avg_positive_decanat': avg_positive_decanat,
        'avg_positive_student': avg_positive_student,
        'avg_speech_decanat': avg_speech_decanat,
        'avg_speech_student': avg_speech_student
    })


def get_student_disciplines(student):
    dict_student = {}
    dict_all = {}
    dict_marks = {5: 0, 4: 0, 3: 0, 2: 0}
    marks = Marks.objects.filter(student=student)
    print(marks)
    for mark in marks:
        if mark.total_score < 56:
            dict_marks[2] += 1
        if 56 <= mark.total_score < 71:
            dict_marks[3] += 1
        if 71 <= mark.total_score < 86:
            dict_marks[4] += 1
        if 86 <= mark.total_score:
            dict_marks[5] += 1
        dict_student[mark.discipline] = mark.total_score
        all_marks = Marks.objects.filter(discipline=mark.discipline)
        total_count = 0
        total_score = 0.0
        for mark in all_marks:
            total_count += 1
            total_score += mark.total_score
        dict_all[mark.discipline] = str(round(total_score / total_count, 2))
    print(list(dict_marks.values()))
    print(list(dict_student.keys()))
    print(list(dict_student.values()))
    return list(dict_student.keys()), list(dict_student.values()), list(dict_all.values()), list(dict_marks.values())


def analyze_total(request):
    students = Students.objects.all()
    student_count = return_if_not_none(len(students), 0)
    most_popular_time = get_most_popular_time_for_all()
    likes_count = Likes.objects.count()
    print(Marks.objects.all().aggregate(Avg('total_score')))
    avg_score = str(round(Marks.objects.all().aggregate(avg=Avg('total_score'))['avg'] or 0.00))
    student_messages_count = Messages.objects.filter(recipient_id=720).count()
    decanat_messages_count = Messages.objects.filter(author=720).count()
    avg_negative_decanat = StudentStatistic.objects.aggregate(avg=Avg('avg_negative_decanat'))['avg'] or 0.00
    print(avg_negative_decanat)
    avg_negative_student = StudentStatistic.objects.aggregate(avg=Avg('avg_negative_student'))['avg'] or 0.00
    avg_neutral_student = StudentStatistic.objects.aggregate(avg=Avg('avg_neutral_student'))['avg'] or 0.00
    avg_neutral_decanat = StudentStatistic.objects.aggregate(avg=Avg('avg_neutral_decanat'))['avg'] or 0.00
    avg_skip_decanat = StudentStatistic.objects.aggregate(avg=Avg('avg_skip_decanat'))['avg'] or 0.00
    avg_skip_student = StudentStatistic.objects.aggregate(avg=Avg('avg_skip_student'))['avg'] or 0.00
    avg_positive_decanat = StudentStatistic.objects.aggregate(avg=Avg('avg_positive_decanat'))['avg'] or 0.00
    avg_positive_student = StudentStatistic.objects.aggregate(avg=Avg('avg_positive_student'))['avg'] or 0.00
    avg_speech_decanat = StudentStatistic.objects.aggregate(avg=Avg('avg_speech_decanat'))['avg'] or 0.00
    avg_speech_student = StudentStatistic.objects.aggregate(avg=Avg('avg_speech_student'))['avg'] or 0.00
    max_scores = list(Marks.objects.all()
                      .values('discipline').annotate(score=Max('total_score')).order_by('discipline')
                      .values_list('score', flat=True))
    min_scores = list(Marks.objects.all()
                      .values('discipline').annotate(score=Min('total_score')).order_by('discipline')
                      .values_list('score', flat=True))
    avg_scores = list(Marks.objects.all()
                      .values('discipline').annotate(score=Avg('total_score')).order_by('discipline')
                      .values_list('score', flat=True))

    disciplines = Marks.objects.all() \
        .values('discipline').annotate(score=Avg('total_score')).order_by('discipline') \
        .values_list('discipline', flat=True)
    discipline_labels = []
    for d in disciplines:
        print(d)
        discipline_labels.append(d)

    d = list(discipline_labels)
    print(d)
    return render(request, 'analyze_total.html', {
        'student_count': student_count,
        'most_popular_time': most_popular_time,
        'likes_count': likes_count,
        'avg_score': avg_score,
        'student_messages_count': student_messages_count,
        'decanat_messages_count': decanat_messages_count,
        'max_scores': max_scores,
        'min_scores': min_scores,
        'avg_scores': avg_scores,
        'discipline_labels': d,
        'avg_negative_decanat': avg_negative_decanat,
        'avg_negative_student': avg_negative_student,
        'avg_neutral_student': avg_neutral_student,
        'avg_neutral_decanat': avg_neutral_decanat,
        'avg_skip_decanat': avg_skip_decanat,
        'avg_skip_student': avg_skip_student,
        'avg_positive_decanat': avg_positive_decanat,
        'avg_positive_student': avg_positive_student,
        'avg_speech_decanat': avg_speech_decanat,
        'avg_speech_student': avg_speech_student
    })


def get_most_popular_time_for_all():
    times = {'День': 0, 'Утро': 0, 'Вечер': 0, 'Ночь': 0}
    statistics = StudentStatistic.objects.all()
    for statistic in statistics:
        if (statistic.most_popular_time):
            times[statistic.most_popular_time] += 1
    return max(times, key=times.get)


def return_if_not_none(v, default):
    if v is not None:
        return v
    else:
        return default


def student_list(request):
    url_parameter = request.GET.get("q")
    if url_parameter:
        students = Students.objects.filter(
            Q(second_name__icontains=url_parameter) |
            Q(first_name__icontains=url_parameter)) \
                       .order_by('student_id')[:10:1]

    else:
        students = Students.objects.order_by('student_id')[:10:1]

    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if is_ajax_request:
        html = render_to_string(
            template_name="student-result-partial.html",
            context={"students": students}
        )
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'student_list.html', {
        'students': students
    })


def median_value(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count % 2 == 1:
        return values[int(round(count / 2))]
    else:
        return sum(values[count / 2 - 1:count / 2 + 1]) / Decimal(2.0)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'analyze_student.html')
        else:
            return render(request, 'registration/login.html',
                          {'error_message': 'Incorrect username and / or password.'})
    else:
        return render(request, 'registration/login.html')
