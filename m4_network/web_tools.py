"""HTTP requests, scraping, and email automation for Module 4 APIs.
Module 4 demonstrates JSON APIs, BeautifulSoup parsing, and SMTP messages.
"""

# CHANGE ME: change this limit to practise scraping a different number of books.
BOOK_LIMIT = 5

import os
import smtplib
from email.message import EmailMessage

import requests
from bs4 import BeautifulSoup

import settings


# CONCEPT: Working with APIs using requests
def fetch_students_from_api():
    """Fetch and print the REST API's student list, or explain a stopped web app."""
    url = "http://%s:%s/api/students" % (settings.HOST, settings.FLASK_PORT)
    try:
        response = requests.get(url, timeout=5)
        students = response.json()
    except requests.exceptions.RequestException:
        print("Start the web app first")
        return []
    for student in students:
        print(student)
    return students


# CONCEPT: Web scraping using BeautifulSoup
def _extract_books(soup, limit):
    """Extract and print the requested number of book titles and prices."""
    books = []
    for article in soup.select("article.product_pod")[:limit]:
        title = article.select_one("h3 a")["title"]
        price = article.select_one("p.price_color").get_text(strip=True)
        books.append((title, price))
        print(title, "-", price)
    return books


def scrape_books(limit=BOOK_LIMIT):
    """Print book titles and prices from the practice scraping site."""
    try:
        response = requests.get(settings.BOOKS_URL, timeout=5)
    except requests.exceptions.RequestException:
        print("Could not fetch books")
        return []
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    return _extract_books(soup, limit)


# CONCEPT: Email automation
def _build_message(subject, body):
    """Create the message used by both test mode and SMTP delivery."""
    message = EmailMessage()
    message["From"] = settings.EMAIL_FROM
    message["To"] = settings.EMAIL_TO
    message["Subject"] = subject
    message.set_content(body)
    return message


def _close_smtp(smtp):
    """Close an SMTP client while ignoring shutdown errors."""
    if smtp is not None and hasattr(smtp, "quit"):
        try:
            smtp.quit()
        except (OSError, smtplib.SMTPException):
            pass


def _send_message(message, password):
    """Send a prepared message and always attempt to close the SMTP client."""
    smtp = None
    try:
        smtp = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        smtp.starttls()
        smtp.login(settings.EMAIL_FROM, password)
        smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as error:
        print("Email could not be sent:", error)
        return False
    finally:
        _close_smtp(smtp)
    return True


def send_email(subject, body):
    """Print an EmailMessage in test mode or send it using an environment password."""
    message = _build_message(subject, body)
    if settings.EMAIL_TEST_MODE:
        print(message)
        return True
    password = os.environ.get("SRM_EMAIL_PASSWORD")
    if not password:
        print("Set SRM_EMAIL_PASSWORD before sending email")
        return False
    return _send_message(message, password)


def demo():
    """Run the API, scraping, and email examples in a friendly order."""
    students = fetch_students_from_api()
    scrape_books()
    if students:
        first = students[0]
        body = "First student: %s" % first
    else:
        body = "No student result was available."
    send_email("Student results", body)


if __name__ == "__main__":
    demo()
