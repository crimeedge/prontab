import google_auth_oauthlib
import googleapiclient.discovery
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from driverMethods import create_driver


def get_api_service():
    api_service_name = "youtube"
    api_version = "v3"
    key = open('.creds').readlines()[0].strip()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)
    return youtube


scope = ["https://www.googleapis.com/auth/youtube"]


def get_authenticated_service(scopes=scope):
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "o.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = run_selenium(flow)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube


def run_selenium(flow, **kwargs):
    kwargs.setdefault('prompt', 'consent')

    flow.redirect_uri = flow._OOB_REDIRECT_URI

    auth_url, _ = flow.authorization_url(**kwargs)

    driver = create_driver()
    driver.get(auth_url)
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.ID, "profileIdentifier"))).click()
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.LINK_TEXT, "Advanced"))).click()
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.LINK_TEXT, "Go to prontab (unsafe)"))).click()
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".M9Bg4d .RveJvd"))).click()
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "#submit_approve_access .RveJvd"))).click()
    code = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.XPATH,
                                        '// *[ @ id = "view_container"] / div / div / div[2] / div / div / div / form '
                                        '/ span / section / div / span / div / div / div / textarea '
                                        ))).text
    driver.quit()
    # code = input(authorization_code_message)

    flow.fetch_token(code=code)

    return flow.credentials
