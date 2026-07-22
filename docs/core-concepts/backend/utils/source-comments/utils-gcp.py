
def read_json_from_gcs(
    bucket_name,
    blob_name,
    gcp_project_id=settings.DATAOPS_PROJECT_ID,
    max_retries=3,
    initial_backoff=0.5,
):
    """
    Helper function to read a JSON file from Google Cloud Storage with retry logic.

    Uses exponential backoff to handle transient failures such as race conditions
    during Terraform state file updates.

    Missing objects (HTTP 404 / ``NotFound``) return ``{}`` immediately — typical when
    Terraform has not written state yet; callers treat empty outputs as "no value".

    Args:
        bucket_name (str): Name of the GCS bucket
        blob_name (str): Path to the blob within the bucket
        gcp_project_id (str): GCP project ID for the storage client
        max_retries (int): Maximum number of retry attempts (default: 3)
        initial_backoff (float): Initial backoff delay in seconds (default: 0.5)

    Returns:
        dict: The parsed JSON content as a dictionary

    Raises:
        Exception: If all retry attempts fail (non-404 errors)
    """


def trigger_cloud_build(trigger_id, project_id, location, substitutions=None):
    """
    Triggers a Cloud Build build using the specified trigger.

    Args:
        trigger_id (str): The ID of the Cloud Build trigger
        project_id (str): The GCP project ID
        location (str): The location of the trigger (e.g., 'us-central1')
        substitutions (dict): A dictionary of substitution variables for the build

    Returns:
        build_obj: The build object if successful, None otherwise
    """


def unique_bucket_name(base_name: str) -> str:
    """
    Generates a unique GCP bucket name from a base string.

    This function ensures the bucket name meets all GCP requirements:
    - 3 to 63 characters long
    - Contains only lowercase letters, numbers, dashes (-), underscores (_), and dots (.)
    - Starts and ends with a letter or number
    - Globally unique (achieved by adding a timestamp and hash suffix)

    Args:
        base_name (str): The base string to create the bucket name from

    Returns:
        str: A valid, unique GCP bucket name

    Raises:
        ValueError: If the base_name is empty or cannot be made valid

    Examples:
        >>> unique_bucket_name("My Project Data")
        'my-project-data-1234567890-a1b2c3'

        >>> unique_bucket_name("Test Bucket!@#")
        'test-bucket-1234567890-d4e5f6'
    """

    # Step 1: Convert to lowercase and replace invalid characters
    # Replace spaces and special characters with dashes
    # Replace any character that's not alphanumeric, dash, underscore, or dot with dash

    # Step 2: Remove consecutive dashes/dots/underscores

    # Step 3: Ensure it starts and ends with alphanumeric
    # Remove leading/trailing non-alphanumeric characters

    # If sanitized is empty after cleaning, use a default

    # Step 4: Generate unique suffix
    # Use timestamp and a short hash for uniqueness
    # Create a short hash from the original base_name and timestamp

    # Step 5: Combine base with unique suffix
    # Format: base-timestamp-hash (ensures uniqueness)

    # Step 6: Ensure length constraints (3-63 characters)
    # Calculate how much we need to trim from the base
    # Keep room for dash + timestamp (10) + dash + hash (6) = 18 chars
    # If even with minimal base we're over limit, use shorter timestamp

    # Final validation
    # This should rarely happen, but handle it

    # Ensure it still starts and ends with alphanumeric after all modifications
    # This shouldn't happen with our logic, but add safety


def sanitize_gcp_project_id(name: str) -> str:
    """
    Converts a user-provided string into a valid GCP project ID.

    GCP project ID requirements:
    - 6 to 20 characters long (project-specific limit)
    - Contains only lowercase letters, numbers, and hyphens
    - Must start with a lowercase letter
    - Cannot end with a hyphen
    - Must be globally unique (not enforced by this function)

    Args:
        name (str): The user-provided string to convert

    Returns:
        str: A valid GCP project ID

    Raises:
        ValueError: If the name is empty or cannot be converted to a valid project ID

    Examples:
        >>> sanitize_gcp_project_id("My Project 2024")
        'my-project-2024'

        >>> sanitize_gcp_project_id("Test_Project!@#123")
        'test-project-123'

        >>> sanitize_gcp_project_id("ABC")
        'abc-project'
    """

    # Step 1: Convert to lowercase

    # Step 2: Replace any character that's not alphanumeric or hyphen with a hyphen

    # Step 3: Remove consecutive hyphens

    # Step 4: Ensure it starts with a lowercase letter
    # Remove leading non-letter characters

    # Step 5: Ensure it doesn't end with a hyphen

    # Step 6: If sanitized is empty or too short after cleaning, handle it

    # Step 7: Truncate to max 20 characters
    # Make sure we didn't end on a hyphen after truncation

    # Step 8: Ensure minimum length of 6 characters
    # Pad with '-project' suffix, but ensure we still start with a letter
