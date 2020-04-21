from django.db.models import Manager


class EnqueueManager(Manager):

    def get_queryset(self):
        return super().get_queryset().exclude(attended=True)
