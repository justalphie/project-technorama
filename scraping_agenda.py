import playwright
import playwright.sync_api
from playwright.sync_api import sync_playwright
import json



url = "https://techorama.be/agenda/"
selector_links = "div.m-subject__container-inner.a-box-simple__inner-2 > a"


#TODO
#1 save the structure [{"time":"...", "activities":[{"name_of_activity":"...", "speaker_name": "...", general_topic": "topic name", "room_number":"..". "url":"...", "date":"...", "time":"time"}]}
#go to each link, and fetch the description and add it to the dictionary
#save a csv


data_technorama = [{"time":"", "activities":[{"name_of_activity":"", "speaker_name": "...", "general_topic": "topic name", "room_number":"..", "url":"...", "date":"...", "time":"time"}]}]
selector_schedule_section = "article.o-schedule__section"
selector_time = "h4.o-schedule__section-title"
selector_activity = "article.m-subject"
selector_activity_title = "h3.m-subject__title"
selector_activity_speaker_name = "p.m-subject__name"
selector_activity_room_number = "p.m-subject__room"
selector_activity_track_label = "p.m-subject__track-label"
selector_url = "div.m-subject__container-inner.a-box-simple__inner-2 > a"

def get_text_content_of(element: playwright.sync_api.ElementHandle):
    if element is None: return None
    return element.text_content()
def get_url_of(element: playwright.sync_api.ElementHandle):
    if element is None: return None
    return element.get_property("href").json_value()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(3000)
    schedule_section_elems = page.query_selector_all(selector_schedule_section)

    sections = []
    for schedule_section_elem in schedule_section_elems:
        section_time = schedule_section_elem.query_selector(selector_time).text_content()
        section_activities = schedule_section_elem.query_selector_all(selector_activity)
        section_activities_list = []
        for section_activity in section_activities:
            activity_name = get_text_content_of(section_activity.query_selector(selector_activity_title))
            speaker_name = get_text_content_of(section_activity.query_selector(selector_activity_speaker_name))
            room_number = get_text_content_of(section_activity.query_selector(selector_activity_room_number))
            track_label = get_text_content_of(section_activity.query_selector(selector_activity_track_label))
            url_activity = get_url_of(section_activity.query_selector(selector_url))
            section_activities_list.append({"name_of_activity": activity_name, 
                "speaker_name": speaker_name, 
                "room_number":room_number,
                "track_label": track_label,
                "url": url_activity,
                "day_of_week":"Tuesday",
                "date": "2024/05/07",
                "time":section_time})
        sections.append({
            "time": section_time,
            "activities": section_activities_list
        })    

    page.locator("button:has-text(\"wednesday\")").click()

    schedule_section_elems = page.query_selector_all(selector_schedule_section)
    for schedule_section_elem in schedule_section_elems:
        section_time = schedule_section_elem.query_selector(selector_time).text_content()
        section_activities = schedule_section_elem.query_selector_all(selector_activity)
        section_activities_list = []
        for section_activity in section_activities:
            activity_name = get_text_content_of(section_activity.query_selector(selector_activity_title))
            speaker_name = get_text_content_of(section_activity.query_selector(selector_activity_speaker_name))
            room_number = get_text_content_of(section_activity.query_selector(selector_activity_room_number))
            track_label = get_text_content_of(section_activity.query_selector(selector_activity_track_label))
            url_activity = get_url_of(section_activity.query_selector(selector_url))
            section_activities_list.append({"name_of_activity": activity_name, 
                "speaker_name": speaker_name, 
                "room_number":room_number,
                "track_label": track_label,
                "url": url_activity,
                "day_of_week":"Wednesday",
                "date": "2024/05/08",
                "time":section_time})
        sections.append({
            "time": section_time,
            "activities": section_activities_list
        })
    # Save sections to JSON file
    with open("sections.json", "w") as f:
        json.dump(sections, f)
    browser.close()

