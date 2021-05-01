import string
import random
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Searching


def random_choice(k: int):
    """
    Creates a random id for room
    Regex: [a-z0-9]{4}\-[a-z0-9]{4}\-[a-z0-9]{4}
    """

    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choices(alphabet, k=k))


@receiver(pre_save, sender=Searching)
def create_id_for_room(update_fields, **kwargs):
    """
    Adds the ID to the model
    """
    if update_fields is not None:
        # doing this to avoid multiple creation of rooms when updating details
        return
    searching_obj: Searching = kwargs.get("instance")
    room_id = random_choice(3) + "-" + random_choice(4) + "-" + random_choice(3)
    searching_obj.room_name = room_id
