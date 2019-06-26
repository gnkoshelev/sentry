"""
sentry.models.counter
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2015 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from django.db import connection

from sentry.db.models import (FlexibleForeignKey, Model, sane_repr, BoundedBigIntegerField)
from sentry.utils.db import is_postgres


class Counter(Model):
    __core__ = True

    project = FlexibleForeignKey('sentry.Project', unique=True)
    value = BoundedBigIntegerField()

    __repr__ = sane_repr('project')

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_projectcounter'

    @classmethod
    def increment(cls, project, delta=1):
        """Increments a counter.  This can never decrement."""
        return increment_project_counter(project, delta)


def increment_project_counter(project, delta=1):
    """This method primarily exists so that south code can use it."""
    if delta <= 0:
        raise ValueError('There is only one way, and that\'s up.')

    cur = connection.cursor()
    try:
        if is_postgres():
            cur.execute(
                '''
                select sentry_increment_project_counter(%s, %s)
            ''', [project.id, delta]
            )
            return cur.fetchone()[0]
        else:
            raise AssertionError("Not implemented database engine path")
    finally:
        cur.close()
