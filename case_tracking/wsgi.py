"""
WSGI config for case_tracking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys



sys.path.append('/var/www/python/case_tracking')
sys.path.append('/var/www/python/case_tracking/case_tracking/lib/python3.8/site-package')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_tracking.settings')


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


