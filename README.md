django-assignment-desk
=====

`django-assignment-desk` is a simple Django app to store and manage weekly editorial staff assignments.

It depends on a staff list (such as the one provided by [`django-editorial-staff`](https://github.com/DallasMorningNews/django-editorial-staff)), and returns a rich API that can be queried by any number of consumers (we're using it to feed both a read-only web interface and a chatbot).

This app uses `django.contrib.postgres`; therefore _it requires a PostgreSQL database and a Python-to-Postgres adapter like `psycopg2` or `psycopg2-binary` to run.

More detailed documentation will be added at a later date.


Quick start
-----------

1. Install this app:

        pip install django-assignment-desk

2.  Add six entries (four helper apps, \"editorial_staff\" and \"assignment_desk\") to your INSTALLED\_APPS setting (in `settings.py`) like this:

        INSTALLED_APPS = [
            ...
            'django.contrib.humanize',
            ...
            'bootstrap3',
            'colorfield',
            'rest_framework',
            ...
            'editorial_staff',
            'assignment_desk',
        ]

    >   **NOTE:** If you already installed `django-editorial-staff`, you may have a number of these in your `INSTALLED_APPS` setting already. They only need to be listed once.

3. Add (or update) the following lines to your `settings.py` file (to configure form rendering):

        BOOTSTRAP3 = {
            'field_renderers': {
                'default': 'bootstrap3.renderers.FieldRenderer',
                'inline': 'bootstrap3.renderers.InlineFieldRenderer',
                'immaterial': 'assignment_desk.field_renderers.ImmaterialFieldRenderer',
            },
        }
    
    >   **NOTE:** Again, these lines only need to be listed once. If you already had similar lines, replace them with the version written here.

4.  Include the editorial_staff and assignment_desk URLconfs in your project's urls.py like this:

        url(r'^staff/', include('editorial_staff.urls')),
        url(r'^assignments/', include('assignment_desk.urls')),

5.  Run `python manage.py migrate` to install the data models into your database.

    >   **NOTE:** As mentioned above, this command will fail if you're not using a PostgreSQL database.

6.  Start the development server and visit
    <http://127.0.0.1:8000/assignments/> to start editing assignments.


Configuration
-------------

You can specify the following configuration options in your project's `settings.py` file. All are optional:

| Setting name                   | Intended value(s)          | Purpose |
|:-------------------------------|:---------------------------|:--------|
| `ASSIGNMENT_DESK_LOGOUT_URL`   | Any reversible URL pattern | If set, includes a "log out" link in the navigation on each `django-assignment-desk` page. |
| `ASSIGNMENT_DESK_DAY_INTERVAL` | Integer (default is 7)     | How many days should be included in an assignment list. |
|||


Front-end development
---------------------

`django-assignment-desk` front-end pages are built using ES6 and SCSS, and this app includes a Gulp installation that converts files written in these dialects to plain JavaScript and CSS, respectively.

When developing on the front-end, you'll need to run this Gulp installation yourself. Follow these steps to get started.

1.  Open a terminal window and navigate to the root of this app.

2.  Within the app, navigate to `./assignment_desk/staticapp`.

3.  If this is your first time running Gulp on this project, run `npm install` to install JS dependencies. This may take several minutes.

4.  Once your dependencies are installed, run `gulp` to begin local development.

5.  When your Gulp server says it's up and running, visit <http://127.0.0.1:3000/assignments/> for a live preview of your front-end files.

6.  Proceed to modify your front-end interface by changing files in `./assignment_desk/staticapp/scss/` and `./assignment_desk/staticapp/js/`. Your changes will be applied to the Gulp server URL without the need for to reload the page manually.
