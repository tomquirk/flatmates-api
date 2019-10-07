# flatmates_api

🏠 Python Wrapper for flatmates.com.au

> No "official" API access required - just use a valid Flatmates account!

### Example usage

1. Log in on the website, and get a _sessionId, _flatmates_session_id and csrf token, then:

```python
api = Flatmates(
    sessionId="abcd",
    flatmatesSessionId="abcd",
    csrfToken="abcd",
)

# search people
people = api.search(location="west-end-4101", min_price=300, max_depth=1)

# send message
person = people[0]
api.send_message(person.get("id"), "Hey man, come live with me")
```
