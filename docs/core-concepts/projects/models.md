class ProjectStatus(models.TextChoices):
    """Status choices for projects."""

    def get_output_value(self, output_name: str) -> str:
        """
        Each project has a Terraform state bucket containing its respective state file.
        The state file is tracked in PROJECT_DEPLOYMENT_STATE_BUCKET.
        The file is in a directory named after the project prefix,
        e.g, /deployments/<project_prefix>-state/default.tfstate.

        Parse the state file into a Python dictionary and return the value of the specified output.

        Args:
            output_name (str): The name of the output to retrieve (e.g., "project_id", "service_account_email")

        Returns:
            str: The output value if found, empty string otherwise
        """

    def generate_project_prefix(self) -> str:
        """
        Generate a unique project prefix (6-20 characters) for the project based on its display name.

        Uses sanitize_gcp_project_id to ensure the prefix meets GCP project ID requirements:
        - Be 6 to 20 characters long
        - Contain only lowercase letters, digits, and hyphens
        - Start with a letter
        - Not end with a hyphen

        If the generated prefix already exists, appends a numeric suffix to ensure uniqueness.

        Returns:
            str: A unique, valid GCP project ID prefix

        Raises:
            ValueError: If unable to generate a unique prefix after 1000 attempts
        """

    @property
    def vertex_notebook_uri(self) -> str:
        """
        Get the Vertex Notebook URI, using cached value if available.
        Falls back to GCS read and caches the result for future requests.
        Returns a dummy value when GCP interactions are disabled.
        """

    @property
    def notebook_sa_email(self) -> str:
        """
        Get the notebook service account email, using cached value if available.
        Falls back to GCS read and caches the result for future requests.
        Returns a dummy value when GCP interactions are disabled.
        """

    @property
    def project_id(self) -> str:
        """
        Get the GCP project ID, using cached value if available.
        Falls back to GCS read and caches the result for future requests.
        Returns a dummy value when GCP interactions are disabled.
        """

    @property
    def network(self) -> str:
        """
        Get the VPC network ID from the project's state file.
        The network ID is stored in the outputs block with name "vpc_id".
        """

    @property
    def subnetwork(self) -> str:
        """
        Get the VPC subnetwork ID from the project's state file.
        The subnetwork ID is stored in the outputs block with name "subnetwork_id".
        """

    @property
    def seqera_service_account_email(self) -> str:
        """
        Get the default service account email from the project's state file.
        The service account email is stored in the outputs block with name "service_account_email".
        """

    @property
    def seqera_output_bucket(self) -> str:
        """
        Get the Seqera output bucket, using cached value if available.
        Falls back to GCS read and caches the result for future requests.
        Returns a dummy value when GCP interactions are disabled.
        """

    def _read_terraform_outputs(self) -> dict:
        """
        Read all Terraform output values from GCS in a single request.

        Returns:
            dict: Extracted output values keyed by output name, or empty dict on failure.
        """

    def _apply_and_save_terraform_cache(self, outputs: dict) -> None:
        """
        Apply transformations to raw Terraform outputs and save all cached fields atomically.

        Transformation logic mirrors the individual property setters:
        - vertex_notebook_uri gets an ``https://`` prefix when missing.
        - seqera_output_bucket is stored without the ``gs://`` prefix (added on read).
        - Empty values fall back to FAILED_TO_GET_OUTPUT when build_status is FAILURE.
        """

    def populate_terraform_cache(self) -> None:
        """
        Proactively populate cached Terraform output values from GCS.
        Call this after Cloud Build completes successfully to warm the cache.

        Reads the Terraform state file once and saves all cached fields in a
        single DB write to avoid race conditions with Django signals.
        """

    def refresh_terraform_cache(self) -> None:
        """
        Force refresh all cached Terraform output values from GCS.
        Clears existing cached values and re-fetches from the Terraform state.
        Use this to manually repopulate the cache when values may have changed.

        Both the clear and the re-populate are performed as atomic single-save
        operations to avoid race conditions with Django signals.
        """

    @property
    def seqera_sa_key(self) -> dict:
        """
        Get the Seqera service account key JSON from GCP Secret Manager.
        The secret is named according to the format <PROJECT_PREFIX>-seqera-sa-key
        and lives in the project specified by CLOUD_BUILD_GCP_PROJECT_ID.

        Returns:
            dict: The service account key as a dictionary, or empty dict if not found
        """

    @property
    def seqera_launchpad_url(self) -> str:
        """
        Get the Seqera Launchpad URL for this project.
        """

    @property
    def has_seqera_workspace(self) -> bool:
        """
        Check if this project has a Seqera workspace.
        Returns False if project opted out of Seqera.
        """

    @property
    def has_seqera_compute_env(self) -> bool:
        """
        Check if this project has a Seqera compute environment.
        """

    def get_users_with_access(self) -> dict[str, str]:
        """
        Get all users who should have access to this project's Seqera workspace.
        This includes:
        1. Project users (from ProjectUser model)
        2. Lab users with appropriate permissions (from LabUser model)

        Returns:
            dict[str, str]: Dictionary mapping user emails to their Seqera workspace roles
            ('admin', 'launch', 'view')
        """

    def get_notebook_users(self) -> set[str]:
        """
        Get all user emails who should have IAM access to this project's notebooks.

        Includes lab directors and all explicit ProjectUser members regardless
        of their permission group.

        Returns:
            set[str]: Set of user email strings.
        """

    def get_notification_users(self):
        """
        Get all users who should be notified about project changes.
        Includes project users and lab directors/readers.

        Returns:
            set: Set of User instances to notify
        """

    def _validate_seqera_config(self) -> bool:
        """
        Validate that Seqera configuration is properly set up.

        Returns:
            bool: True if configuration is valid, False otherwise
        """

    def _get_workspace_member_info(self, seqera_client: SeqeraClient) -> dict:
        """
        Get current workspace members and their information.

        Args:
            seqera_client: The Seqera client to use

        Returns:
            dict: Dictionary mapping email to member info, or empty dict if failed
        """

    def _add_or_update_member(
        self,
        seqera_client: SeqeraClient,
        email: str,
        role: str,
        workspace_member_info: dict,
    ) -> bool:
        """
        Add a new member or update an existing member's role.

        Args:
            seqera_client: The Seqera client to use
            email: The email of the user to add/update
            role: The role to assign
            workspace_member_info: Current workspace member information

        Returns:
            bool: True if operation was successful, False otherwise
        """

    def _remove_member(
        self,
        seqera_client: SeqeraClient,
        email: str,
        participant_id: str,
    ) -> bool:
        """
        Remove a member from the workspace.

        Args:
            seqera_client: The Seqera client to use
            email: The email of the user to remove
            participant_id: The participant ID of the user to remove

        Returns:
            bool: True if removal was successful, False otherwise
        """

    def sync_seqera_workspace_access(self) -> bool:
        """
        Synchronize project users with Seqera workspace access.
        This ensures that all users with access to the project (through any means)
        have access to the Seqera workspace and removes access for users who
        no longer have access to the project.

        Returns:
            bool: True if sync was successful, False otherwise
        """
