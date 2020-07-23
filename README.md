
* ~$ sudo apt-get install python3.5
* ~$ sudo apt-get install python3-pip
* ~$ sudo apt-get install python3-venv
* ~$ git clone https://github.com/EZELKOC/quora-django.git
* ~$ cd quora-django/
* ~$ python3 -m venv env
* ~$ cd env/bin/source activate

Tekra projenin bulunduğu dizine gelin ve bu komutları terminalde çalıştırın.

* (env) ~$ pip install --upgrade pip
* (env) ~$ pip install -r requirements.txt
* (env) ~$ python manage.py migrate
* (env) ~$ python manage.py runserver

Django yu daha iyi anlamak için https://tutorial.djangogirls.org/tr/ sitesine bakmanızı önemle rica ediyorum.
