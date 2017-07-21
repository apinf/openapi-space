# OpenAPI space
![Build Status](https://travis-ci.org/apinf/openapi-space.svg?branch=master)

A backend for storing OpenAPI specifications
## Setup
0. Have Python 3.5 or higher installed. Lower python 3.x versions may or may not work.

### Automated, dev environment
1. Run the setup script (`./setup.sh`)
2. Run the server (`./start.sh`)

### Automated, Docker
1. Build the image (`docker build . -t openapi-space`)
2. Run  `docker run -p <port>:80 openapi-space` replacing `<port>` with the port you want the app to be accessible at.
3. OpenAPI space should now be accessible at `http://localhost:<port>`

### Manual
1. Install virtualenv
2. Create a virtualenv (`virtualenv -p /path/to/python3 venv`)
3. Enter the virtualenv (`source venv/bin/activate`)
4. Install dependencies (`pip install -r requirements.txt`)
5. Start the server
   * Development mode: `python main.py`
   * uWSGI: `uwsgi --ini uwsgi.ini`
