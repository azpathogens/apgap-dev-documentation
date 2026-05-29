class SourceType(models.Model):
    """
    Stores various sample source types
    """


class MetadataRequirement(models.Model):
    """
    Configurable table that defines which metadata keys are required
    for which source types. Null source type means required for all source types
    """

    # TODO: Delete this model and all views associated with it
    #  /\_/\ call me out in code review
    # ( o.o )
    #  > ^ <
    # confirm that no endpoints relating to it are being used in the application


class MetadataTemplate(models.Model):
    """
    Configurable table that defines the metadata template for a given source type
    """

    def __str__(self):
        """Return a string representation of the template."""

    def save(self, *args, **kwargs):
        """Set name to key.name if name is not provided."""

    def clean(self):
        """
        prevent core/non-core key name collisions accross templates
        """


class MetadataTemplateOption(models.Model):
    """
    Configurable table that defines the options for a given metadata template
    """

    def __str__(self):
        """Return a string representation of the template option."""
