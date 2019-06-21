## How to run
I recommend creating a virtual environment
* Linux 
``python3 -m venv /path/to/new/virtual/environment``
* Windows
``python -m venv c:\path\to\myenv``

Install required packages from requirements.txt
``pip install -r requirements.txt``

Create database and migrate
* Linix ``python3 manage.py migrate``
* Windows ``python manage.py migrate``

Run localhost
* Linix ``python3 manage.py runserver``
* Windows ``python manage.py runserver``

Specially selected SqlLitle to be able to send you a pre-populated database 
with an admin account. For easier start.

Credentials to admin panel:
`login: admin, password:admin`

## Librares and database
I used three libraries for this project:
* django==2.2.2 (I don't think, that I need to explain why I used the django framework)
* djangorestframework==3.9.2 (The most popular library/framework to creating REST API in Django.
 Is a powerful and flexible toolkit for building Web APIs)

I think that for such a simple and small one does not need a better database.
The principle of using this database from another (from the django level) does not differ too much, because we use django ORM anyway.

How we can read in django documentation.
"SQLite provides an excellent development alternative for applications 
that are predominantly read-only or require a smaller installation footprint." 

## How to use
* `GET /event/` - Displays the list of all events already present in application database. 
You can ordering by any movie field. [How to?](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

* `GET /top` - Return all events with available ticket and prices for different (ticket) types. 
    Prices are assumed in euro 

* `GET /reserve` - You must enter `id` reservation to se details for eg.`reserve/?id=1`,
otherwise you will receive `"error": "Pass reservation id"`. If you pass wrong `id` you will receive
`"error": "Reservation with the given id does not exist"`.

* `POST /reserve` - To create reservation, you should to pass `first_name_client`, `last_name_client`, `email`
 `phone_number`, `event` and `type_ticket` in request.

* `GET /statistics` - Return statistics. IMPORTANT only bought bought are counted!!!
For each event you can get info about number of ticket for every types.
In last element in list, you can get information total number of ticket in every types.

* `POST /pay` I must admit that I did not know how to use the component prepared by you sensibly.
I decided that the payment system is a dummy for the task. Probably the shape and functionality of this component 
would depend on the external API of the popular payment system.
    
    But how to used it?
    To correct pay for your ticket you should pass `amount`, `currency` in euro and your `reservation_id`

To create events and types of ticket use django admin panel.
##### Reservation is valid for 15 minutes:

I decided that using cron for every minutes is not provide to good performance and is stupid.
That's why every time you download information about reservations and tickets,
system updates reservation state.

##### What is missing:
* Validation fields
* Protection against unwanted events
* Better and more extensive tests, larger coverage
* More real business logic
* Security -> Hide the secret key, hide the eventual database password, debug set on false
###### Post Scriptum:
I tried to stick to pep8, but i know that many things are often arranged within the project,
 e.g. the length of the line so I believe in your mercy in this topic ;) 



