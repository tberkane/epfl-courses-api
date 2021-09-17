from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values
config = dotenv_values('epfl-courses-api/.env')

client = MongoClient(
    config['DB_URL'])
db = client.epfl_courses.courses

db.drop()  # reset db

URL_BASE = 'https://edu.epfl.ch/'
page = requests.get(URL_BASE + 'studyplan/en/master/')
soup = BeautifulSoup(page.content, 'html.parser')

links = soup.main.ul
for link in links.contents:
    data = []

    # page with links to section pages
    link_page = requests.get(URL_BASE + link.a['href'])
    link_soup = BeautifulSoup(link_page.content, 'html.parser')

    group_elements = [g for g in link_soup.find_all(  # course groups
        'div', class_='study-plan-master')]
    for (i, group_element) in enumerate(group_elements):
        course_elements = group_element.find_all('div', class_='line-down')
        for course_element in course_elements:
            name_element = course_element.find('div', class_='cours-name')
            info_element = course_element.find('div', class_='cours-info')
            teacher_element = course_element.find(
                'div', class_='enseignement-name')
            exam_element = course_element.find('div', class_='exam-text')

            group = str(i) + ' ' + group_element.h4.text
            if name_element.a:
                name = name_element.a.text
                name_link = URL_BASE + name_element.a['href']
            else:
                name = name_element.parent['data-title']
                name_link = ''

            code = info_element.text.split()[0]
            # deal with courses which have no code (such as shs)
            if code == '/':
                code = ''
            section = info_element.text.split()[-1]
            teachers = [a.text for a in teacher_element.find_all('a')]
            teacher_links = [a['href'] for a in teacher_element.find_all('a')]

            language = course_element.find('div', class_='langue').abbr.text
            if exam_element.b:
                semester = 'Fall' if exam_element.b.text == 'Winter session' else 'Spring'
            else:
                semester = ''
            exam_type = exam_element.span.text
            if exam_type == 'During the semester':
                exam_type = 'Semester'

            hours_element = course_element.div.contents[
                2] if semester == 'Fall' else course_element.div.contents[3]
            hours = [int(h.text[0]) if h.text[-1] ==  # remove the 'h' in hours and change '-' to 0
                     'h' else 0 for h in hours_element.find_all('div', class_='cep')]

            spec_element = course_element.find('ul', class_='spec')
            specializations = [
                s.text for s in spec_element] if spec_element else []

            credits = int(course_element.find(
                'div', class_='credit-time').text)

            course = {'name': name, 'link': name_link, 'code': code, 'section': section,
                      'teachers': teachers, 'teacher_links': teacher_links,
                      'language': language, 'semester': semester, 'exam_type': exam_type, 'hours': hours, 'specializations': specializations, 'credits': credits, 'group': group}

            if name_element.i:
                # remove parentheses around remark
                course['remark'] = name_element.i.text[1:-1].strip().capitalize()

            data.append(course)
    if data:
        # only keep last part of url
        db[link.a['href'].split('/')[-2]].insert_many(data)
