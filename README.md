# OpenAPI space
A backend for storing OpenAPI specifications

## Setup
0. Have Python 3.5 or higher installed. Lower python 3.x versions may or may not work.

### Automated, dev environment
1. Run the setup script (`./setup.sh`)
2. Run the server (`./start.sh`)

### Automated, Docker
TODO

### Manual
1. Install virtualenv
2. Create a virtualenv (`virtualenv -p /path/to/python3 venv`)
3. Enter the virtualenv (`source venv/bin/activate`)
4. Install dependencies (`pip install -r requirements.txt`)
5. Start the server
  * Development mode: `python main.py`
  * uWSGI: `uwsgi --ini uwsgi.ini`
