from celery import shared_task

from .models import Profile, Relationship


@shared_task
def refresh_people():
    """The function removes all skipped users from the profile relationships.
    So that they appear again in the users feed.
    This task will be executed every 12 hours.
    """

    # Get all skipped relationships
    relationships = Relationship.objects.filter(like=False, match=False)

    # And delete them
    for rel in relationships:
        rel.delete()
