import json
from flatmates_api import Flatmates

api = Flatmates(
    sessionId="abcd",
    flatmatesSessionId="abcd",
    csrfToken="abcd",
)

# search people
people = api.search(location="west-end-4101", min_price=300, max_depth=1)

# send message
person = people[0]
error = api.send_message(person.get("memberId"), "Hi :)")
if error:
    print(f'Error sending message to {person.get("memberId")}')