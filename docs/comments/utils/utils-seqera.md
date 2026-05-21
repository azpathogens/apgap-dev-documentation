
def slugify(name: str) -> str:
    """Convert a string into a valid Seqera resource name.

    Args:
        name: The string to convert

    Returns:
        A string with only alphanumeric characters and dashes, between 2 and 39 characters long,
        starting with a letter. Spaces and special characters are converted to dashes, and
        multiple dashes are collapsed into one.
    """


class SeqeraClient:
    """
    Client for interacting with Seqera Cloud API.
    """

    def _log_request(self, method: str, url: str, payload: dict | None = None, headers: dict | None = None):
        """Helper method to log request details"""

    def _log_response(self, response: requests.Response):
        """Helper method to log response details"""

    def create_workspace(  # noqa: C901
        self,
        organization_id: str,
        name: str,
        description: str | None = None,
        full_name: str | None = None,
        visibility: str = "PRIVATE",
    ) -> dict[str, Any]:
        """
        Create a new workspace in the specified organization.

        Args:
            organization_id: The ID of the organization to create the workspace in
            name: The name of the workspace (must be unique within the organization)
            description: Optional description of the workspace
            full_name: Optional full name of the workspace
            visibility: Workspace visibility, default is 'PRIVATE'

        Returns:
            Dict containing the created workspace information or None if an error occurs
        """

    def create_compute_environment(  # noqa: PLR0913
        self,
        workspace_id: str,
        name: str,
        platform: str,
        config: dict[str, Any],
        description: str | None = None,
        credentials_id: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a compute environment for a workspace.

        Args:
            workspace_id: The ID of the workspace to create the compute environment in
            name: The name of the compute environment
            platform: The platform (e.g., 'gls', 'aws', 'azure', 'gcp')
            config: Dictionary with platform-specific configuration
            description: Optional description
            credentials_id: The ID of the credentials to use with the compute environment

        Returns:
            Dict containing the created compute environment information or None if an error occurs
        """

    def create_gcp_compute_environment(  # noqa: PLR0913
        self,
        workspace_id: str,
        name: str,
        service_account_email: str,
        project_id: str,
        region: str = "us-central1",
        work_dir: str = "gs://workdir",
        description: str | None = None,
        spot: bool = False,  # noqa: FBT001, FBT002
        use_private_address: bool = True,  # noqa: FBT001, FBT002
        network: str | None = None,
        subnetwork: str | None = None,
        wave_enabled: bool = False,  # noqa: FBT001, FBT002
        fusion_enabled: bool = False,  # noqa: FBT001, FBT002
    ) -> dict[str, Any]:
        """
        Create a GCP Batch-specific compute environment for a workspace.
        Only includes fields that have non-null values in the configuration.

        Args:
            workspace_id: The ID of the workspace to create the compute environment in
            name: The name of the compute environment
            service_account_email: The service account email for the GCP compute environment
            project_id: The GCP project ID
            region: The GCP region, default is 'us-central1'
            work_dir: The work directory (bucket path) for the compute environment
            description: Optional description
            spot: Whether to use spot instances, default is False
            use_private_address: Whether to use private IP addresses, default is True
            network: VPC network name
            subnetwork: VPC subnetwork name
            wave_enabled: Whether to enable Wave, default is False
            fusion_enabled: Whether to enable Fusion2, default is False

        Returns:
            Dict containing the created compute environment information or None if an error occurs
        """

    def get_workspace(self, organization_id: str, workspace_id: str) -> dict[str, Any] | None:
        """
        Get details for a specific workspace.

        Args:
            workspace_id: The ID of the workspace to retrieve

        Returns:
            Dict containing the workspace information or None if an error occurs
        """

    def delete_workspace(self, organization_id: str, workspace_id: str) -> bool:
        """
        Delete a Seqera workspace.

        Args:
            organization_id: The ID of the organization containing the workspace
            workspace_id: The ID of the workspace to delete

        Returns:
            True if deletion was successful, False otherwise
        """

    def get_compute_environment(self, workspace_id: str, compute_env_id: str) -> dict[str, Any] | None:
        """
        Get details for a specific compute environment.

        Args:
            workspace_id: The ID of the workspace
            compute_env_id: The ID of the compute environment to retrieve

        Returns:
            Dict containing the compute environment information or None if an error occurs
        """

    def create_credentials(
        self,
        workspace_id: str,
        name: str,
        provider: str,
        credentials: dict[str, Any],
        description: str | None = None,
    ) -> dict[str, Any] | str | None:
        """
        Create credentials in a Seqera workspace for a specific provider.

        Args:
            workspace_id: The ID of the workspace
            name: The name of the credentials
            provider: The provider (e.g., "google", "aws", "azure")
            credentials: The credentials data
            description: Optional description

        Returns:
            The credentials data (dict), credential ID (str), or None if an error occurs
        """

    def create_data_link(  # noqa: PLR0913
        self,
        workspace_id: str,
        name: str,
        description: str | None,
        provider: str,
        resource_ref: str,
        public_accessible: bool = False,  # noqa: FBT001, FBT002
        credentials_id: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Create a data link in a Seqera workspace.

        Args:
            workspace_id: The ID of the workspace to create the data link in
            name: The name of the data link
            description: Optional description of the data link
            provider: The provider (e.g., "google", "aws", "azure")
            resource_ref: The resource reference (e.g., bucket name for GCS)
            public_accessible: Whether the data link is publicly accessible
            credentials_id: Optional ID of credentials to use with the data link

        Returns:
            Dict containing the created data link information or None if an error occurs
        """

    def delete_data_link(
        self,
        workspace_id: str,
        data_link_id: str,
    ) -> bool:
        """
        Delete a data link from a Seqera workspace.

        Args:
            workspace_id: The ID of the workspace containing the data link
            data_link_id: The ID of the data link to delete

        Returns:
            True if deletion was successful, False otherwise
        """

    def list_data_links(
        self,
        workspace_id: str,
    ) -> list[dict[str, Any]] | None:
        """
        List all data links in a Seqera workspace.

        Args:
            workspace_id: The ID of the workspace to list data links from

        Returns:
            List of data link dictionaries or None if an error occurs
        """

    def get_organization(self, organization_id: str) -> dict[str, Any] | None:
        """
        Get details for a specific organization.

        Args:
            organization_id: The ID of the organization to retrieve

        Returns:
            Dict containing the organization information or None if an error occurs
        """

    def add_workspace_member(
        self,
        organization_id: str,
        workspace_id: str,
        email: str,
        role: str = "launch",
    ) -> dict[str, Any] | None:
        """
        Add a participant to a Seqera workspace and optionally promote them to admin.
        Participants are given the "launch" role by default.

        Args:
            organization_id: The ID of the organization
            workspace_id: The ID of the workspace
            email: The email of the user to add
            role: The role to assign (owner, admin, maintain, launch, connect, view)

        Returns:
            Dict containing the participant information or None if an error occurs
        """

    def update_workspace_participant_role(
        self,
        organization_id: str,
        workspace_id: str,
        participant_id: int,
        role: str,
    ) -> bool:
        """
        Update a participant's role in a Seqera workspace.

        Args:
            organization_id: The ID of the organization
            workspace_id: The ID of the workspace
            participant_id: The ID of the participant to update
            role: The new role to assign (owner, admin, maintain, launch, connect, view)

        Returns:
            True if the role update was successful, False otherwise
        """

    def remove_workspace_member(
        self,
        organization_id: str,
        workspace_id: str,
        participant_id: int,
    ) -> bool:
        """
        Remove a participant from a Seqera workspace.

        Args:
            organization_id: The ID of the organization
            workspace_id: The ID of the workspace
            participant_id: The ID of the participant to remove

        Returns:
            True if removal was successful, False otherwise
        """

    def list_workspace_members(
        self,
        organization_id: str,
        workspace_id: str,
    ) -> list[dict[str, Any]] | None:
        """
        List all participants of a Seqera workspace.

        Args:
            organization_id: The ID of the organization
            workspace_id: The ID of the workspace

        Returns:
            List of participant dictionaries or None if an error occurs.
            Each participant dict contains:
            - participantId: int
            - memberId: int
            - userName: str
            - firstName: str | None
            - lastName: str | None
            - email: str
            - orgRole: str
            - teamId: int | None
            - teamName: str | None
            - wspRole: str
            - type: str
            - teamAvatarUrl: str | None
            - userAvatarUrl: str | None
        """
