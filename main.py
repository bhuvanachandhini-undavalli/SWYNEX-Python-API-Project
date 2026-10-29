
"""Fetch and display users from a public REST API."""

import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://jsonplaceholder.typicode.com/users"
MAX_USERS = 5
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class APIError(Exception):
    """Raised when an API request or response is invalid."""


def validate_users(data):
    if not isinstance(data, list) or len(data) < MAX_USERS:
        raise APIError("Invalid API data: expected at least five users.")

    users = []

    for user in data:
        if not isinstance(user, dict):
            raise APIError("Invalid user data.")

        name = user.get("name")
        email = user.get("email")

        if not isinstance(name, str) or not name.strip():
            raise APIError("A user has an invalid name.")

        if not isinstance(email, str) or not EMAIL_PATTERN.fullmatch(email.strip()):
            raise APIError("A user has an invalid email.")

        users.append({"name": name.strip(), "email": email.strip()})

    return users


def fetch_users():
    request = Request(
        API_URL,
        headers={"Accept": "application/json"}
    )

    try:
        with urlopen(request, timeout=10) as response:
            if not 200 <= response.status < 300:
                raise APIError(f"HTTP error: {response.status}")
            data = json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        raise APIError(f"HTTP error: {error.code}") from error
    except URLError as error:
        raise APIError(f"Connection error: {error.reason}") from error
    except TimeoutError as error:
        raise APIError("Request timed out.") from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise APIError("Invalid API response.") from error

    return validate_users(data)


def main():
    try:
        answer = input("How many users? Enter 1-5 (default 5): ").strip()
        count = 5 if not answer else int(answer)

        if not 1 <= count <= 5:
            print("Please enter a number from 1 to 5.")
            return

        users = fetch_users()

        print("\nSWYNEX PYTHON API PROJECT")
        print("-" * 30)

        for number, user in enumerate(users[:count], start=1):
            print(f"{number}. {user['name']} - {user['email']}")

    except ValueError:
        print("Error: Please enter a whole number.")
    except APIError as error:
        print(f"Error: {error}", file=sys.stderr)
    except (KeyboardInterrupt, EOFError):
        print("\nProgram cancelled.")


if __name__ == "__main__":
    main()
