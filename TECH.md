OpenAPI Space is a Python program built with Flask and Connexion
* The primary objective is to provide access to a Swagger spec database through a REST API.
* [Flask](http://flask.pocoo.org/) is a microframework for building Python based web servers. We concluded that it fits well into building a backend where the main function is to provide a REST API.
  * [Connexion](https://github.com/zalando/connexion) is a framework used on top of Flask. It allows taking the next step into design first API building, by automatically mapping endpoints when given an API specification in OpenAPI 2.0 format.
* Integrates into Apinf platform authentication by using the login API of the platform.
