import os
import requests
import pandas as pd

from bs4 import BeautifulSoup

from dotenv import load_dotenv

LOGIN_URL = "https://witkac.pl/Account/Login"
TABLE_URL = "https://witkac.pl/Contest/IndexTableData"
CONTEST_URL_PREFIX = "https://witkac.pl/contest/view?id="

# Load environment variables
load_dotenv()
WITKAC_LOGIN = os.getenv("WITKAC_LOGIN")
WITKAC_PASSWORD = os.getenv("WITKAC_PASSWORD")

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

def get_grants_table(session) -> pd.DataFrame:

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
    df = pd.DataFrame(data["data"])
    # print other keys
    print(data_page.json().keys())

    # print sample of the data
    print(df.sample(10))

    # save the data to csv in ./data/metadata with current date in the name
    df.to_csv(f"./data/metadata/witkac_{pd.Timestamp.now().date()}.csv", index=False)

    return df


def get_single_grant_page(session,grant_id) -> dict:
    # get single grant page, but wait to be redirected
    grant_page = session.get(f"{CONTEST_URL_PREFIX}{grant_id}", allow_redirects=True)
    # print request headers
    print("Request headers:")
    print(grant_page.request.headers)
    # check status code
    if grant_page.status_code != 200:
        raise Exception("Grant page request failed")
    # print status code
    print(grant_page.status_code)
    # print the page url
    print(grant_page.url)
    # print the response headers
    print("Response headers:")
    print(grant_page.headers)
    soup = BeautifulSoup(grant_page.content, "html.parser")
    # search for div with id h3
    print(soup)
    


if __name__ == "__main__":
    grant_id = 30801
    session = get_witkac_auth_session()
    get_single_grant_page(session,grant_id)