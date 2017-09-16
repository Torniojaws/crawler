# Installation

## Prerequisites

- Python 3.5+ (the async await features *require* at least 3.5)
- Pip 3 (should come with Python 3)
- virtualenv (should come with Python 3)

## Notes

Out of the box, the site requirements are defined in the file
[site-requirements.txt](site-requirements.txt), But you can also change it to use some online
resource.

## Setup in NIX

1. Go to the project root in a terminal
1. (Optional) Create a virtualenv for Python with: ``virtualenv venv``
1. (Optional) Activate the virtualenv with: ``source venv/bin/activate``
1. Check that you have pip3 with: ``pip -V`` - it should say Python 3.x in the output
1. Install the project Python packages with: ``pip install -r requirements/dev.txt``
1. Once all have been installed successfully, launch with
    ``python app.py -p 60 -r site-requirements.txt``
1. You should see output in the console, and also in the file ``logs/crawl_log.txt`` within the
project directory.

## Setup in Windows

This has been tested in PowerShell

1. Go to the project root
1. (Optional) Create a virtualenv for Python with: ``virtualenv venv``
1. (Optional) Activate the virtualenv. In PowerShell, you might need to run this first:
    ``set-executionpolicy RemoteSigned`` and then run: ``venv\Scripts\activate.ps1``
1. Check that you have pip3 with: ``pip -V``, it should say Python 3.x in the output
1. Then install the project depedencies with: ``pip install -r requirements\dev.txt``
1. Once all have been installed successfully, launch with:
    ``python app.py -p 60 -r site-requirements.txt``
1. You should see output in the console, and also in the file ``logs/crawl_log.txt`` within the
project directory.
