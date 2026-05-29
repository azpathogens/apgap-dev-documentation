
class CloudBuildClient:
    """
    Client for interacting with Google Cloud Build API.
    """

    def trigger_build(self, trigger_id, project_id, location, substitutions=None):
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

    def get_build_status(self, build_id, project_id, location):
        """
        Get the status of a Cloud Build build.

        Args:
            build_id (str): The ID of the build
            project_id (str): The GCP project ID
            location (str): The location of the build (e.g., 'us-central1')

        Returns:
            str: The status of the build, or None if there was an error
        """

    def is_build_complete(self, status):
        """
        Check if the build status indicates the build is complete.

        Args:
            status (str): The build status from Cloud Build API

        Returns:
            bool: True if the build is complete, False otherwise
        """

    def is_build_successful(self, status):
        """
        Check if the build status indicates the build was successful.

        Args:
            status (str): The build status from Cloud Build API

        Returns:
            bool: True if the build was successful, False otherwise
        """


class CloudBuildClientOfficial:
    """
    Client for interacting with Google Cloud Build API using the official Google client library.

    This implementation provides better error handling, automatic retries, and more detailed
    error messages compared to the REST-based implementation.
    """

    def _extract_build_info_from_operation(self, operation):
        """
        Extract build information from Cloud Build operation.

        Args:
            operation: The operation returned from run_build_trigger

        Returns:
            dict: Build object with id and status formatted for compatibility
        """

    def _extract_build_id(self, build):
        """Extract build ID from Build object."""

    def _extract_build_status(self, build):
        """Extract and convert build status from Build object."""

    def _extract_build_info_using_result(self, operation):
        """
        Extract build information by waiting for operation to complete.
        This follows the exact pattern from Google's documentation.

        Args:
            operation: The operation returned from run_build_trigger

        Returns:
            dict: Build object with id and status formatted for compatibility
        """

    def trigger_build(self, trigger_id, project_id, location, substitutions=None):
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
        # Prepare the request according to the API documentation
        # The 'name' field should be the full resource name
        # The 'source' field contains substitutions for the build

        # Call the API - returns a google.api_core.operation.Operation

        # Validate we got an operation back

        # Extract build information from the operation
        # Try the documented way first (using result()), then fall back to metadata

        # Log success
    def get_build_status(self, build_id, project_id, location):
        """
        Get the status of a Cloud Build build.

        Args:
            build_id (str): The ID of the build
            project_id (str): The GCP project ID
            location (str): The location of the build (e.g., 'us-central1')

        Returns:
            str: The status of the build, or None if there was an error
        """

    def is_build_complete(self, status):
        """
        Check if the build status indicates the build is complete.

        Args:
            status (str): The build status from Cloud Build API

        Returns:
            bool: True if the build is complete, False otherwise
        """

    def is_build_successful(self, status):
        """
        Check if the build status indicates the build was successful.

        Args:
            status (str): The build status from Cloud Build API

        Returns:
            bool: True if the build was successful, False otherwise
        """
