**_Frontend is not implemented yet_**


**Setup**
1) create a python virtual environment
2) install the dependencies using `python -m pip install -r requirements.txt`
3) generate a django secret key using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
4) add the secret key to the project as shown here https://stackoverflow.com/questions/64208678/hiding-secret-key-in-django-project-on-github-after-uploading-project
5) initialize the sqllite database with `python manage.py makemigrations` and `python manage.py migrate`
6) run the django api using `python manage.py runserver`


**Django-React Notes and Lessons Learned**
- When you create a Django app (not same as Django project), add the path('api/', include('api.urls') at the project level project/urls.py
- Admin site is very useful for adding and looking at data:
  - Register your models in admin.py you can view and interact with them in the admin site.
  - Whenever models are added to the admin site they don't have names, this can be fixed by creating admin.ModelAdmin classes.
  - Tables referenced as foreign keys will need to implement __str__ method to properly show data in the admin site.
- Keep models in one file.
- ManyToManyField reduced large amounts of code to access intermediary tables.
- Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.
- Enable CORS (download corsheaders and add configs in the settings.py) and allow CORS from Frontend endpoint (http://localhost:3000/).
  - CorsMiddleware config in the settings should be placed above the CommonMiddleware
- Authorization:
  - Use Django User model to create users; either using existing users or new users
  - Enable Token based authentication and provide tokens to all existing users.
  - Use the token in all your requests
  - Post requests will always require tokens otherwise you will run into CSRF errors
  - sessionid cookie required for SessionAuthentication can be created using Django's login(request, user) function.
  - Specify all the types of authentication you will use in settings.py
- Add API endpoint to React/Axios getters and setter methods to be able to ping the backend.
- Identify which npm packages need to be global to work properly. Main example: npm -g install npm
- There are react dev tools for the browser.
