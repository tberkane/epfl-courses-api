from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re

client = MongoClient(
    'mongodb+srv://tberkane:43QcccltS7Y89I2D@cluster0.07kae.mongodb.net/epfl_courses?retryWrites=true&w=majority')
collection = client.epfl_courses.courses

collection.drop()  # reset db

url = 'https://edu.epfl.ch/studyplan/en/master/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

links = soup.main.ul
for link in links.contents:
    print(link.a['href'])
    data = []
    page = requests.get('https://edu.epfl.ch/' + link.a['href'])
    soup = BeautifulSoup(page.content, 'html.parser')

    group_elements = [g for g in soup.find_all(
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
                name_link = 'https://edu.epfl.ch/' + name_element.a['href']
            else:
                name = name_element.parent['data-title']
                name_link = ''

            code = info_element.text.split()[0]
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

            """ hours_element = course_element.find(
                attrs={'data-title': 'Master ' + ('1' if semester == 'Fall' else '2')}) """
            hours_element = course_element.div.contents[2] if semester == 'Fall' else course_element.div.contents[3]
            hours = [int(h.text[0]) if h.text[-1] ==
                    'h' else 0 for h in hours_element.find_all('div', class_='cep')]

            spec_element = course_element.find('ul', class_='spec')
            specializations = [
                s.text for s in spec_element] if spec_element else []

            credits = int(course_element.find('div', class_='credit-time').text)

            course = {'name': name, 'link': name_link, 'code': code, 'section': section,
                    'teachers': teachers, 'teacher_links': teacher_links,
                    'language': language, 'semester': semester, 'exam_type': exam_type, 'hours': hours, 'specializations': specializations, 'credits': credits, 'group': group}

            if name_element.i:
                course['remark'] = name_element.i.text[1:-1].strip().capitalize()

            data.append(course)
    if data:
        collection[link.a['href'].split('/')[-2]].insert_many(data)
