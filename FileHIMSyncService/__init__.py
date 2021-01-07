
"""tasks.py is the file to hold all celery relates tasks
 using rabbit-mq as the message broker.
"""

from .celery import app as celery_app

__all__ = ['celery_app']