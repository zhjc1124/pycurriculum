from pycurriculum import Curriculum, Course
from UIMS import UIMS
import re


def generate_ics(user, pwd, filename):
    start_date, courses = UIMS(user, pwd).get_course()
    course_lists = []
    for course in courses:
        course_info = {}
        c = course['teachClassMaster']
        if c['lessonSchedules']:
            course_info['name'] = c['lessonSegment']['fullName']
            course_info['teacher'] = c['lessonTeachers'][0]['teacher']['name']
            course_info['schedule'] = []
            for s in c['lessonSchedules']:
                schedule = [s['classroom']['fullName']]
                time = s['timeBlock']
                week = '一二三四五六日'
                values = re.findall('周([%s])第(\d*)[,\d]*,(\d*)节\{第(\d*)-(\d*)周(\|(.)周)?\}' % week, time['name'])[0]
                schedule.append('%s-%s-%s' % (week.index(values[0]) + 1, values[1], values[2]))
                repeat = '%s-%s' % (values[3], values[4])
                if values[-1] == '单':
                    repeat += '-1'
                elif values[-1] == '双':
                    repeat += '-2'
                schedule.append(repeat)
                course_info['schedule'].append(schedule)
            course_lists.append(course_info)
    curriculum = Curriculum(start_date)
    for c in course_lists:
        curriculum.add(Course(**c))
    curriculum.to_ics(filename)


if __name__ == '__main__':
    username, password = input('请输入用户名和密码（用","分隔开）：').split(',')
    generate_ics(username, password, 'mycourses')
