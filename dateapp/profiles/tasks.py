from celery import task, shared_task

from .models import Profile, Relationship


@shared_task
def refresh_people():
    """
    The function removes all skipped users from the profile relationships.
    So that they appear again in the users feed.
    This task will be executed every 12 hours.
    """

    # Get all skipped relationships
    relationships = Relationship.objects.filter(like=False, match=False)

    # And delete them
    for rel in relationships:
        rel.delete()


@task
def reset_like(user_id, target_id):
    """
    Resets the like to the user if there is no match.
    Called a week after the like.
    """
    user = Profile.objects.get(id=user_id)
    target = Profile.objects.get(id=target_id)
    rel = Relationship.objects.filter(user=user, target=target).first()
    if not rel.match:
        rel.delete()