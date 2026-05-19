"""
Utility functions for checking user permissions and roles.
"""


def is_platform_admin(user):
    """
    Check if user is a Platform Administrator or superuser.

    Checks superuser status, boolean field, and group membership.

    Args:
        user: User instance

    Returns:
        bool: True if user is Platform Admin or superuser, False otherwise
    """


def is_lab_director(user, lab=None):
    """
    Check if user is a Lab Director.

    If lab is provided, checks if user is Lab Director for that specific lab.
    If lab is None, checks if user is Lab Director for any lab.

    Args:
        user: User instance
        lab: Optional Lab instance

    Returns:
        bool: True if user is Lab Director, False otherwise
    """


def is_lab_collaborator(user, lab=None):
    """
    Check if user is a Lab Collaborator (or Lab Reader).

    Lab Reader maps to Lab Collaborator per plan requirements.
    If lab is provided, checks if user is Lab Collaborator for that specific lab.
    If lab is None, checks if user is Lab Collaborator for any lab.

    Args:
        user: User instance
        lab: Optional Lab instance

    Returns:
        bool: True if user is Lab Collaborator, False otherwise
    """


def is_bioinformatics_user(user, project=None):
    """
    Check if user is a Bioinformatics User.

    If project is provided, checks if user is Bioinformatics User for that specific project.
    If project is None, checks if user is Bioinformatics User for any project.

    Args:
        user: User instance
        project: Optional Project instance

    Returns:
        bool: True if user is Bioinformatics User, False otherwise
    """


def is_data_analyst(user):
    """
    Check if user is a Data Analyst.

    Checks both boolean field and group membership.

    Args:
        user: User instance

    Returns:
        bool: True if user is Data Analyst, False otherwise
    """


def has_lab_access(user, lab):
    """
    Check if user has any access to a lab.

    User has access if they are:
    - Platform Admin
    - Lab Director for the lab
    - Lab Collaborator for the lab
    - Member of a project in the lab

    Args:
        user: User instance
        lab: Lab instance

    Returns:
        bool: True if user has lab access, False otherwise
    """


def has_project_access(user, project):
    """
    Check if user has any access to a project.

    User has access if they are:
    - Platform Admin
    - Lab Director for the project's lab
    - Lab Collaborator for the project's lab
    - Member of the project

    Args:
        user: User instance
        project: Project instance

    Returns:
        bool: True if user has project access, False otherwise
    """


def get_user_labs(user):
    """
    Get all labs the user has access to.

    Args:
        user: User instance

    Returns:
        QuerySet: QuerySet of Lab instances
    """


def get_user_projects(user, lab=None):
    """
    Get all projects the user has access to.

    Args:
        user: User instance
        lab: Optional Lab instance to filter projects

    Returns:
        QuerySet: QuerySet of Project instances
    """
