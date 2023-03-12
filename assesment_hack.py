import django
import os
import random
import argparse
from django.core.exceptions import ObjectDoesNotExist


COMMENDATIONS = [
 'Молодец!',
 'Отлично!',
 'Хорошо!',
 'Гораздо лучше, чем я ожидал!',
 'Ты меня приятно удивил!',
 'Великолепно!',
 'Прекрасно!',
 'Ты меня очень обрадовал!',
 'Именно этого я давно ждал от тебя!',
 'Сказано здорово – просто и ясно!',
 'Ты, как всегда, точен!',
 'Очень хороший ответ!',
 'Талантливо!',
 'Ты сегодня прыгнул выше головы!',
 'Я поражен!',
 'Уже существенно лучше!',
 'Потрясающе!',
 'Замечательно!',
 'Прекрасное начало!',
 'Так держать!',
 'Ты на верном пути!',
 'Здорово!',
 'Это как раз то, что нужно!',
 'Я тобой горжусь!',
 'С каждым разом у тебя получается всё лучше!',
 'Мы с тобой не зря поработали!',
 'Я вижу, как ты стараешься!',
 'Ты растешь над собой!',
 'Ты многое сделал, я это вижу!',
 'Теперь у тебя точно все получится!'
]


class ToManySchoolkids(Exception):
    pass


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(child, subject_name):
    year_of_study = child.year_of_study
    subject = Subject.objects.filter(title=subject_name, year_of_study=year_of_study).first()
    lessons = Lesson.objects.filter(subject=subject)
    lesson = random.choice(lessons)
    text = random.choice(COMMENDATIONS)
    Commendation.objects.create(
        text=text,
        created=lesson.date,
        schoolkid=child,
        subject=subject,
        teacher=lesson.teacher
    )


def check_child(child):
    if child.count() == 1:
        return child.first()
    if not child:
        raise ObjectDoesNotExist
    if child.count() > 1:
        raise ToManySchoolkids


def create_parser():
    parser = argparse.ArgumentParser(
        description='hack shool database'
    )
    parser.add_argument('-n', '--name', help='Имя ученика', default='Фролов Иван')
    parser.add_argument('-s', '--subject', help='Название предмета', default='Математика')
    parser.add_argument('-f', help='Исправить оценки', action="store_true", default=False)
    parser.add_argument('-r', help='Убрать замечания', action="store_true", default=False)
    parser.add_argument('-c', help='Добавить похвалу', action="store_true", default=False)
    return parser


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    django.setup()
    parser = create_parser()
    args = parser.parse_args()

    from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation
    child = Schoolkid.objects.filter(full_name__contains=args.name)
    try:
        child = check_child(child)
        if args.f:
            fix_marks(child)
        if args.r:
            remove_chastisements(child)
        if args.c:
            create_commendation(child, args.subject)
    except ToManySchoolkids:
        print('Найденно несколько учеников с данным именнем')
    except ObjectDoesNotExist:
        print('Ученик не найден.')
