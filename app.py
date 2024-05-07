import json
import time
import streamlit as st
import requests
import pandas as pd
import datetime as dt
from io import StringIO

# set page config
st.set_page_config(page_title="LearnApp", page_icon="favicon.png")

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




