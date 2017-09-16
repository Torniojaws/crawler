# Crawler

Load a predefined list of URLs and content requirements for each URL, and then
call them periodically to check their availability. The content requirement
must also be satisfied.

The results are logged along with the time it took from the start of the
request until it was completed. If the site was down, it will be marked as
"down" in the log file. If the site did not match the content requirement,
then it will be marked as "No match". If both are satisfied, the log is marked
as "ok".

## Run

Start with: ``python app.py --period 60 --req site-requirements.txt``. This will check the sites
every 60 seconds and uses the rules defined in the local file ``site-requirements.txt`` in the
root of this project.

You can also define an URL: ``python app.py --period 60 --req https://www.example.com/my-rules.txt``

If no time period is given, a default value of 60 seconds is used.

You can also use shortcut flags:
``-p`` == ``--period``
``-r`` == ``--req``

## Installation

See the [install instructions](INSTALL.md)

## To-do

See the [TODO list](TODO.md)

## Tests

Run the tests with: ``python -m pytest tests``.
If you want the coverage report too, run:
``python -m pytest --cov-report term-missing --cov=apps tests/``
