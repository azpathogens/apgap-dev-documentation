class Lab(models.Model):

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
        Generate a unique project prefix (6-20 characters) for the lab based on its display name.

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
    def project_id(self) -> str:
        """
        Get the GCP project ID, using cached value if available.
        Falls back to GCS read and caches the result for future requests.
        Returns a dummy value when GCP interactions are disabled.
        """

    def populate_terraform_cache(self) -> None:
        """
        Proactively populate cached Terraform output values from GCS.
        Call this after Cloud Build completes successfully to warm the cache.
        """

    def refresh_terraform_cache(self) -> None:
        """
        Force refresh all cached Terraform output values from GCS.
        Clears existing cached values and re-fetches from the Terraform state.
        Use this to manually repopulate the cache when values may have changed.
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
