=============================
django-currentwateruser
=============================

----

.. contents:: Conveniently store reference to request wateruser on thread/db level.

----

Quickstart
----------

Install django-currentwateruser::

    pip install django-currentwateruser

Add it to the middleware classes in your settings.py::

    MIDDLEWARE = (
        ...,
        'django_currentwateruser.middleware.ThreadLocalWaterUserMiddleware',
    )

Then use it in a project::

    from django_currentwateruser.middleware import (
        get_current_wateruser, get_current_authenticated_wateruser)

    # As model field:
    from django_currentwateruser.db.models import CurrentWaterUserField
    class Foo(models.Model):
        created_by = CurrentWaterUserField()
