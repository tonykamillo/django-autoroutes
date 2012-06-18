# Django autoroutes

A simple module that makes your life easier by creating automatically routes your django project.

# Instalation
```bash
$ pip install django-autoroutes
```
or download/clone the package and

```bash
$ python setup.py install
```

# Usage

Add the ROOT_DIR option in settings.py 
```python
ROOT_DIR = '/absolute/path/to/my/project/dir'
```

and change the file urls.py of the project so that it looks like that is below

```python
import django_autoroutes

urlpatterns = django_autoroutes.patterns()
```
Done, just create your apps and have fun.
