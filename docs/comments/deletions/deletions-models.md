class ArchiveRequest(TimeStampedModel):
    """
    Model to track archive requests for any object in the system.
    Uses GenericForeignKey to reference any model instance.
    Supports an approval workflow with Lab Director review.
    """


class Deletion(models.Model):
    """
    Model to track deletions of any object in the system with justification.
    Uses GenericForeignKey to reference any model instance.
    """

    def save(self, *args, **kwargs):
        """
        Override save to capture object representation before deletion.
        """
