@receiver(pre_save, sender=Organization)
def notify_data_governance_on_default_approval_enabled(sender, instance, **kwargs):
    """
    Send an email to the Data Governance Group when an organization
    enables auto-approval of reportable-pathogen access requests.
    """
