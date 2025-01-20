import os

import requests

from genezio import genezio_deploy, genezio_login, genezio_local
from utils import kill_process
from playwright.sync_api import sync_playwright
import random
import string
import psycopg2


def confirmEmail(email: str):
    print("Confirming email " + email + "...")
    result = psycopg2.connect(os.environ.get('AUTH_TEST_DB_URL'))
    cursor = result.cursor()
    cursor.execute('SELECT "tokenConfirmEmail" FROM users WHERE email = %s', (email,))
    result = cursor.fetchone()
    cursor.close()

    webhook_url = os.environ.get('CONFIRM_EMAIL_WEBHOOK_URL') + "?token=" + result[0]
    response = requests.get(webhook_url).status_code
    return response == 200


def resetPassword(email: str):
    print("Resetting password for email " + email + "...")
    webhook = os.environ.get('RESET_PASSWORD_WEBHOOK_URL') + "?email=" + email

    if requests.get(webhook).status_code != 200:
        return None

    result = psycopg2.connect(os.environ.get('AUTH_TEST_DB_URL'))
    cursor = result.cursor()
    cursor.execute('SELECT "tokenReset" FROM users WHERE email = %s', (email,))
    result = cursor.fetchone()
    cursor.close()
    print("Token reset ", result[0])
    return result[0]


def test_react_auth():
    print("Starting React Auth test...")
    token = os.environ.get('GENEZIO_TOKEN')

    os.chdir(os.path.join("projects", "react-auth-runtime"))

    genezio_login(token)

    deploy_result = genezio_deploy(False)

    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    process = genezio_local()

    assert process != None, "genezio local returned None"
    kill_process(process)

    frontend_link = [url[0] for url in deploy_result.stdout_all_links if 'amber-wide-ant' in url[0]]
    print("Frontend link: " + frontend_link[0])

    gmail = "".join(random.choices(string.ascii_lowercase, k=6)) + "@gmail.com"
    password = "P".join(random.choices(string.ascii_lowercase, k=6)) + "12!"

    # Test signup page
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(frontend_link[0] + "/signup")
        page.get_by_label("Name:").click()
        page.get_by_label("Name:").fill("".join(random.choices(string.ascii_uppercase, k=4)))
        page.get_by_label("Name:").press("Tab")
        page.get_by_label("Email:").fill(gmail)
        page.get_by_label("Email:").press("Tab")
        page.get_by_label("Password:").fill(password)
        page.get_by_role("button", name="Sign Up").click()
        try:
            page.wait_for_timeout(10000)
        except TimeoutError:
            assert False, "Timeout occured while waiting for signup page"
        assert page.url == frontend_link[0] + "/login", "Signup failed"
        browser.close()

    # Test email confirmation
    assert confirmEmail(gmail), "Email confirmation failed"

    # Test login page
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(frontend_link[0] + "/login")
        page.get_by_label("Email:").click()
        page.get_by_label("Email:").fill(gmail)
        page.get_by_label("Password:").click()
        page.get_by_label("Password:").fill(password)
        page.get_by_role("button", name="Login").click()
        try:
            page.wait_for_timeout(10000)
        except TimeoutError:
            assert False, "Timeout occured while waiting for login"
        page.get_by_role("button", name="Reveal Secret").click()
        assert page.inner_text(
            "text='Capybaras are AWESOME! Shhh... don't tell the cats!'") == "Capybaras are AWESOME! Shhh... don't tell the cats!", "Get secret failed"
        # Test logout button
        page.get_by_role("button", name="Logout").click()
        try:
            page.wait_for_timeout(10000)
        except TimeoutError:
            assert False, "Timeout occured while waiting for logout"
        assert page.url == frontend_link[0] + "/login", "Logout failed"
        browser.close()

    # Test reset password
    token = resetPassword(gmail)
    password = "P".join(random.choices(string.ascii_lowercase, k=6)) + "12!"
    assert token != None, "Reset password failed"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(frontend_link[0] + "/reset" + "?token=" + token)
        page.get_by_placeholder("password", exact=True).click()
        page.get_by_placeholder("password", exact=True).fill(password)
        page.get_by_placeholder("re-enter password").click()
        page.get_by_placeholder("re-enter password").fill(password)
        page.get_by_role("button", name="Reset Password").click()
        try:
            page.wait_for_timeout(10000)
        except TimeoutError:
            assert False, "Timeout occured while waiting for reset password"
        assert page.url == frontend_link[0] + "/login", "Reset password failed"
        browser.close()

    # Test login with new password
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(frontend_link[0] + "/login")
        page.get_by_label("Email:").click()
        page.get_by_label("Email:").fill(gmail)
        page.get_by_label("Password:").click()
        page.get_by_label("Password:").fill(password)
        page.get_by_role("button", name="Login").click()
        try:
            page.wait_for_timeout(10000)
        except TimeoutError:
            assert False, "Timeout occured while waiting for login"
        page.get_by_role("button", name="Reveal Secret").click()
        assert page.inner_text(
            "text='Capybaras are AWESOME! Shhh... don't tell the cats!'") == "Capybaras are AWESOME! Shhh... don't tell the cats!", "Get secret failed at login with new password"
        browser.close()
    print("Test passed!")


if __name__ == '__main__':
    test_react_auth()
