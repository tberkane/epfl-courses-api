from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

client = MongoClient(
    "mongodb+srv://tberkane:43QcccltS7Y89I2D@cluster0.07kae.mongodb.net/epfl_courses?retryWrites=true&w=majority")
collection = client.epfl_courses.courses

collection.drop()

data = []

url = "https://edu.epfl.ch/studyplan/en/master/computer-science/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

group1 = soup.find("h4", string="Group 1").parent
course_elements = group1.find_all("div", class_="line-down")
for course_element in course_elements:
    name_element = course_element.find("div", class_="cours-name")
    info_element = course_element.find("div", class_="cours-info")
    teacher_element = course_element.find("div", class_="enseignement-name")
    exam_element = course_element.find("div", class_="exam-text")

    name = name_element.a.text
    link = name_element.a['href']
    code = info_element.text.split()[0]
    section = info_element.text.split()[-1]
    teachers = [a.text for a in teacher_element.find_all("a")]
    teacher_links = [a['href'] for a in teacher_element.find_all("a")]

    language = course_element.find("div", class_="langue").abbr.text

    semester = "Fall" if exam_element.b.text == "Winter session" else "Spring"
    exam_type = exam_element.span.text

    hours_element = course_element.find(
        attrs={"data-title": "Master " + ("1" if semester == "Fall" else "2")})
    print(course_element)
    hours = [int(h.text[0]) if h.text[-1] ==
             "h" else 0 for h in hours_element.find_all("div", class_="cep")]
    
    specializations = [s.text for s in course_element.find("ul", class_="spec").contents]
    
    credits = int(course_element.find("div", class_="credit-time").text)

    data.append({"name": name, "link": link, "code": code, "section": section,
                "teachers": teachers, "teacher_links": teacher_links,
                 "language": language, "semester": semester, "exam_type": exam_type, "hours": hours, "specializations": specializations, "credits": credits})

print(data)

collection.insert_many(data)
