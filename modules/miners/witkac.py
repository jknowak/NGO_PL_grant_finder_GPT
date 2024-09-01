import os
import requests

from bs4 import BeautifulSoup

from credentials import WITKAC_LOGIN, WITKAC_PASSWORD

LOGIN_URL = "https://witkac.pl/Account/Login"
TABLE_URL = "https://witkac.pl/Contest/IndexTableData"

def get_request_load_dict(start=0, length=100):
    load = {}
    columns = ["Tytul", "NazwaOrganu", "TerminSkladania", "WysokoscSrodkow", "Id"]
    for i in range(5):
        load[f"columns[{i}][data]"] = columns[i]
        load[f"columns[{i}][name]"] = ""
        load[f"columns[{i}][searchable]"] = "true"
        load[f"columns[{i}][orderable]"] = "true"
        load[f"columns[{i}][search][value]"] = ""
        load[f"columns[{i}][search][regex]"] = "false"
    load["order[0][column]"] = "0"
    load["order[0][dir]"] = "asc"
    load["start"] = start
    load["length"] = length
    load["search[value]"] = ""
    load["search[regex]"] = "false"
    load["urzad"] = ""
    load["departament"] = ""
    load["filter"] = "1"
    load["yearStart"] = "2024"
    load["yearEnd"] = "2025"
    load["sferaPP"] = "-1"
    load["terc"] = ""
    load["czyWszystkie"] = "False"

    return load


def get_witkac_auth_session():
    # Create a session
    session = requests.Session()

    # Get the login page
    login_page = session.get(LOGIN_URL)

    # Parse the login page
    soup = BeautifulSoup(login_page.content, "html.parser")

    # Prepare the login data
    login_data = {
        "ReturnUrl": "",
        "Email": WITKAC_LOGIN,
        "Password": WITKAC_PASSWORD,
        "rememberme": "true"
    }

    # Post the login data
    login_response = session.post(LOGIN_URL, data=login_data)

    # check status code
    if login_response.status_code != 200:
        raise Exception("Login failed")

    # Return the session cookie
    return session

def get_witkac_data():
    # Get the authenticated session
    session = get_witkac_auth_session()

    # Post the load dict to table url with session cookie
    data_page = session.post(TABLE_URL, data=get_request_load_dict())

    # check status code
    if data_page.status_code != 200:
        raise Exception("Data request failed")
    # Parse the json response
    data = data_page.json()
    
    # get data.data as dataframe
    data = data["data"]
    # print other keys
    print(data_page.json().keys())

if __name__ == "__main__":
    get_witkac_data()