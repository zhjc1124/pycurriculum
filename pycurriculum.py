from datetime import datetime, timedelta, time, date


def check_key(func):
    def wrapper(self, *args, **kwargs):
        if not self._has_key(args[0]):
            raise KeyError('key "%s" is illegal' % args[0])
        return func(self, *args, **kwargs)
    return wrapper


class Course(object):
    def __init__(self, *args, **kwargs):
        self._registry = {'name': None,
                          'teacher': None,
                          'schedule': None,
                          }
        flag = 0
        keys = ['name', 'teacher', 'schedule']
        for key in keys:
            if key in kwargs:
                self._registry[key] = kwargs[key]
            elif flag < len(args):
                self._registry[key] = args[flag]
                flag += 1

    def __str__(self):
        return str(self._registry)
    __repr__ = __str__

    def set(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

    @check_key
    def __setattr__(self, key, value):
        if key == '_registry':
            self.__dict__[key] = value
            return
        self._registry[key] = value

    __setitem__ = __setattr__

    @check_key
    def __getattr__(self, key):
        return self._registry[key]
    __getitem__ = __getattr__

    def _has_key(self, key):
        if key == '_registry' or key in self._registry:
            return True
        else:
            return False


class Curriculum(object):
    def __init__(self, term_start, **kwargs):
        self. courses = []
        self.setting = {'term_start': term_start,
                        'break_time': 10,
                        'after_class': 20,
                        'morning': '8:00',
                        'afternoon': '13:30',
                        'evening': '18:30'}
        if kwargs:
            self.set(**kwargs)

    def __str__(self):
        return '\n'.join(map(str, self.courses))
    __repr__ = __str__

    def set(self, **kwargs):
        if kwargs and kwargs.keys() < self.setting.keys():
            self.setting.update(kwargs)
        else:
            raise KeyError('key %s is illegal' % (kwargs.keys()-self.setting.keys()))

    def add(self, course):
        if type(course.schedule[0]) is str:
            course.schedule = [course.schedule]
        self.courses.append(course)

    def to_ics(self, filename):
        filename += '.ics'
        with open(filename, 'w', encoding='utf8') as f:
            f.write('BEGIN:VCALENDAR\n')
            f.write('PRODID:-//zhjc1124 //pycurriculum 2.0//EN\n')
            f.write('VERSION:2.0\n')
            f.write('CALSCALE:GREGORIAN\n')

            setting = self.setting
            term = date(*map(int, setting['term_start'].split('-')))
            # 变成周一
            term = term - timedelta(days=term.weekday())

            morning = datetime.combine(term, time(*map(int, setting['morning'].split(':'))))
            afternoon = datetime.combine(term, time(*map(int, setting['afternoon'].split(':'))))
            evening = datetime.combine(term, time(*map(int, setting['evening'].split(':'))))

            interval = timedelta(seconds=(90+setting['break_time']+setting['after_class'])*60)
            class_time = {1: morning,
                          3: morning + interval,
                          5: afternoon,
                          7: afternoon + interval,
                          9: evening
                          }

            for course in self.courses:
                for class_ in course.schedule:
                    weekday, begin_class, end_class = map(int, class_[1].split('-'))
                    sub = end_class - begin_class

                    begin_week, end_week, *kind = map(int, class_[2].split('-'))
                    count = end_week - begin_week + 1

                    byday = ('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU')

                    duration = (sub+1) * 45 + sub * setting['break_time']
                    if sub >= 2:
                        duration += setting['after_class'] - 10

                    dtstart = class_time[begin_class] + timedelta(days=(begin_week-1)*7+weekday-1)
                    if kind:
                        kind = kind[0]
                        count = int(count/2)
                        if kind % 2 != begin_week % 2:
                            dtstart += timedelta(days=7)

                    dtend = dtstart + timedelta(seconds=duration*60)
                    f.write('BEGIN:VEVENT\n')
                    f.write(dtstart.strftime('DTSTART:%Y%m%dT%H%M%S\n'))
                    f.write(dtend.strftime('DTEND:%Y%m%dT%H%M%S\n'))
                    f.write('SUMMARY:%s\n' % course.name)
                    f.write('LOCATION:%s  %s\n' % (class_[0], course.teacher))
                    f.write('DESCRIPTION:%s - %s节\n' % (begin_class, end_class))
                    rrule = 'RRULE:FREQ=WEEKLY;COUNT=%s;BYDAY=%s\n' % (count, byday[weekday-1])
                    if kind:
                        rrule = 'RRULE:FREQ=WEEKLY;COUNT=%s;INTERVAL=2;BYDAY=%s\n' % (count, byday[weekday - 1])
                    f.write(rrule)
                    f.write('END:VEVENT\n')
            f.write('END:VCALENDAR\n')


if __name__ == "__main__":
    #            课程名   教室   教师  周一34节  4-10周单周
    t2 = Course('课程二', '刘', ['梁', '2-1-4', '1-20-1'])
    tc = Curriculum('2018-01-01')
    tc.add(t2)
    print(t2.schedule)
