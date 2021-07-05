"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
#import sys
#import django

from django.core.wsgi import get_wsgi_application

#from medtagger.downloadArticles import getArticles

#sys.path.append('medtagger_dashboard/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medtagger_dashboard.settings')

#django.setup()

#getArticles('catatonic schizophrenia', '200')

application = get_wsgi_application()
