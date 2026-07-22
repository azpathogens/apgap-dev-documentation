def set_user_permissions(user, permissions_with_content_types_tuples):
    """
    Set permissions for a user given
    a list of permission and content type tuples.

    Args:
        user: User object
        permissions_with_content_types_tuples:
        List of tuples of
        permissions and content types,
        formatted like:
        [("permission", ContentTypeClass),]

    Returns:
        User object with permissions added
    """
