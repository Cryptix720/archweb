#!/usr/bin/python
import os
import sys
import site

base_path = "/srv/http/archweb"

site.addsitedir('/srv/http/archweb-env/lib/python2.7/site-packages')
sys.path.insert(0, base_path)

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

os.chdir(base_path)

using_newrelic = False
try:
    import newrelic.agent
    from newrelic.api.exceptions import ConfigurationError
    try:
        newrelic.agent.initialize(os.path.join(base_path, "newrelic.ini"))
        using_newrelic = True
    except ConfigurationError:
        pass
except ImportError:
    pass

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

if using_newrelic:
    _application = application
    def application(environ, start_response):
        os.environ["NEW_RELIC_LICENSE_KEY"] = environ.get("NEW_RELIC_LICENSE_KEY", None)
        return _application(environ, start_response)

    application = newrelic.agent.wsgi_application()(application)
