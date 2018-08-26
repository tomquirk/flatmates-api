# linkedin_api

👨‍💼 Python Wrapper for the Linkedin API

> No "official" API access required - just use a valid Linkedin account!

Programmatically send messages, perform searchs, get profile data and more, all with only your Linkedin account!

##### USE AT YOUR OWN RISK 😉
This project should only be used as a learning project. Using it would violate Linkedin's Terms of Use. I am not responsible for your account being blocked (which they will definitely do. Hint: **don't use your personal Linkedin account**)

## Overview

This project attempts to provide a simple Python interface for the Linkedin API.

> Do you mean the [legit Linkedin API](https://developer.linkedin.com/)?

NO! To retrieve structured data, the [Linkedin Website](https://linkedin.com) uses a service they call **Voyager**. Voyager endpoints give us access to pretty much everything we could want from Linkedin: profiles, companies, connections, messages, etc.

So specifically, this project aims to provide complete coverage for Voyager.

[How do we do it?](#in-depth-overview)

### Want to contribute?
[How do I find endpoints?](to-find-endpoints)

## Installation
```
$ pip install linkedin-api
```

### Example usage

```python
from linkedin_api import Linkedin

# Authenticate using any Linkedin account credentials
api = Linkedin('reedhoffman@linkedin.com', 'iheartmicrosoft')

# GET a profile
profile = api.get_profile('billy-g')

# GET a profiles contact info
contact_info = api.get_profile_contact_info('billy-g')

# GET all connected profiles (1st, 2nd and 3rd degree) of a given profile
connections = api.get_profile_connections('1234asc12304', max_connections=200)
```

## Documentation
For a complete reference documentation, see the [DOCS.md](https://github.com/tomquirk/linkedin-api/blob/master/DOCS.md)

## Setup

### Dependencies

* Python 3
* A valid Linkedin user account (don't use your personal account, if possible)
* Pipenv (optional)

1. Using pipenv...

    ```
    $ pipenv install
    $ pipenv shell
    ```

## In-depth overview

Voyager endpoints look like this:
```
https://www.linkedin.com/voyager/api/identity/profileView/tom-quirk
```

Or, more clearly
```
 ___________________________________ _______________________________
|             base path             |            resource           |
https://www.linkedin.com/voyager/api /identity/profileView/tom-quirk
```

They are authenticated with a simple cookie, which we send with every request, along with a bunch of headers.

To get a cookie, we POST a given username and password (of a valid Linkedin user account) to `https://www.linkedin.com/uas/authenticate`.

### To find endpoints...

We're looking at the Linkedin website and we spot some data we want. What now?

The most reliable method to find the relevant endpoint is to: 
1. `view source`
2. `command-f`/search the page for some keyword in the data. This will exist inside of a `<code>` tag.
3. Scroll down to the **next adjacent element** which will be another `<code>` tag, probably with an `id` that looks something like
    ```html
    <code style="display: none" id="datalet-bpr-guid-3900675">
      {"request":"/voyager/api/identity/profiles/tom-quirk/profileView","status":200,"body":"bpr-guid-3900675"}
    </code>
    ```
4. The value of `request` is the url! :woot:

You can also use the `network` tab in you browsers developer tools, but you will encounter mixed results.

### How Clients query Voyager

Linkedin seems to have developed an internal query language/syntax where Clients (i.e. front-ends like linkedin.com) to specify what data they want (similar to the GraphQL concept). **If anyone knows what this is, I'd love to know!**.

Here's an example of making a request for an organisation's `name` and `groups` (the Linkedin groups it manages):

```
/voyager/api/organization/companies?decoration=(name,groups*~(entityUrn,largeLogo,groupName,memberCount,websiteUrl,url))&q=universalName&universalName=linkedin
```

The "querying" happens in the `decoration` parameter, which looks like
```
(
    name,
    groups*~(entityUrn,largeLogo,groupName,memberCount,websiteUrl,url)
)
```
So here, we request an organisation name, and a list of groups, where for each group we want `largeLogo`, `groupName`, etc.

Different endpoints use different parameters (and perhaps even different syntaxes) to specify these queries. Notice that the above query had a parameter `q` whose value was `universalName`; the query was then specified with the `decoration` parameter. 

In contrast, the `/search/cluster` endpoint uses `q=guided`, and specifies its query with the `guided` parameter, whose value is something like
```
List(v->PEOPLE)
```

It could be possible to document (and implement a nice interface for) this query language - as we add more endpoints to this project, I'm sure it will become more clear if such a thing would be possible (and if it's worth it).

