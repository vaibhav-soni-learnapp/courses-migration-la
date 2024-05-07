import json
import time
import streamlit as st
import requests
import pandas as pd
import datetime as dt
from io import StringIO

# set page config
st.set_page_config(page_title="LearnApp")

# hide streamlit branding and hamburger menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.write("")
with col2:
    st.image("logo.png", width=225)
    st.write("")
with col3:
    st.write("")

st.write("----")

st.markdown(
    "<h2 style='text-align: center; color: white;'>Module Completion Calculator</h2>",
    unsafe_allow_html=True,
)
st.write("----")

# Kraken Auth Token
# functions for getting user specific course progress
url = "https://e3d72bp6aa.execute-api.ap-south-1.amazonaws.com/"
payload = {}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
access_token = response.text

token = "Bearer " + access_token

# Function to get the data of all the courses, classes, workshops and advanced courses on LearnApp
# @st.cache()
def get_learnapp_content():

    url = "https://catalog.prod.learnapp.com/catalog/discover"

    payload = {}
    headers = {"authorization": token, "x-api-key": "ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu"}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)

    courses_data = []
    for i in range(len(data["courses"])):
        for j in range(len(data["courses"][i]["items"])):
            courses_data.append(data["courses"][i]["items"][j])

    classes_data = []
    for i in range(len(data["webinars"])):
        for j in range(len(data["webinars"][i]["items"])):
            classes_data.append(data["webinars"][i]["items"][j])

    workshops_data = []
    for i in range(len(data["workshops"])):
        for j in range(len(data["workshops"][i]["items"])):
            workshops_data.append(data["workshops"][i]["items"][j])

    advcourses_data = []
    for i in range(len(data["advCourses"])):
        for j in range(len(data["advCourses"][i]["items"])):
            advcourses_data.append(data["advCourses"][i]["items"][j])

    learnapp_data = []

    for i in courses_data:
        learnapp_data.append(i)

    for i in classes_data:
        learnapp_data.append(i)

    for i in workshops_data:
        learnapp_data.append(i)

    for i in advcourses_data:
        learnapp_data.append(i)

    final_data = {}

    for i in learnapp_data:

        title = i["title"]
        contentType = i["contentType"]
        canonicalTitle = i["canonicalTitle"]
        id = i["id"]
        totalPlaybackTime = i["totalPlaybackTime"]
        try:
            assetUrl = (
                f"https://assets.learnapp.com/{i['assets']['card-238x165-jpg']['url']}"
            )
        except:
            assetUrl = "https://la-course-recommendation-engine.s3.ap-south-1.amazonaws.com/Basics+of+Trading.jpeg"

        field_data = {
            canonicalTitle: {
                "title": title,
                "canonicalTitle": canonicalTitle,
                "id": id,
                "totalPlaybackTime": totalPlaybackTime,
                "assetUrl": assetUrl,
                "contentType": contentType,
            }
        }

        final_data.update(field_data)

    return final_data




# Function to get the key of any value in dictionary
def get_key(val):
    for key, value in courses.items():
        if val == value:
            return key


# Code for fetching LA data and selecting the courses in the cohort
content_data = get_learnapp_content()
content_data.update(
    {
        "intro-to-trading-terminal": {
            "title": "Intro to Trading Terminal",
            "canonicalTitle": "intro-to-trading-terminal",
            "id": "4fde29ab-6122-46fa-8247-19c26dccb25c",
            "totalPlaybackTime": 4918,
            "assetUrl": "https://assets.learnapp.com/catalog/courses/4fde29ab-6122-46fa-8247-19c26dccb25c/b63ad44d-e3fb-42aa-b7b4-cf474019f4bb.jpeg",
            "contentType": "courses",
        },
        "which-type-of-trader-are-you": {
            "title": "Which type of trader are you?",
            "canonicalTitle": "which-type-of-trader-are-you",
            "id": "ad2b81ed-b70f-43fc-a3e0-040f46f5f287",
            "totalPlaybackTime": 1155,
            "assetUrl": "https://assets.learnapp.com/catalog/workshops/ad2b81ed-b70f-43fc-a3e0-040f46f5f287/2a5f4959-b790-4355-9e63-36a153070349.jpeg",
            "contentType": "workshop",
        },
    }
)

content_type = st.multiselect("Select Content Type",["courses","classes","workshops","advanced-courses"])
selected_content_data = {key:content_data[key] for key in content_data if content_data[key]["contentType"] in content_type}


courses = {}

courses_list = st.multiselect(
    "Create a module by selecting any course/class/workshop/advanced course",
    selected_content_data.keys(),
)

courses = {i: selected_content_data[i]["id"] for i in selected_content_data if i in courses_list}
st.write("")

