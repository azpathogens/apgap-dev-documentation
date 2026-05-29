  @property
   def batch_sa_key(self) -> dict:
        """
        Get the batch service account key JSON from GCP Secret Manager.
        The secret is stored in the project's GCP project and named according to
        the format stored in batch_service_account_secret_name.

        Returns:
            dict: The service account key as a dictionary, or empty dict if not found
        """

    def get_file_size(self):
        """
        Get the size of all files in the dataset.
        """

    def get_file_preview(self, preview_limit=3):
        """
        Get a preview of files for this dataset and the total file count.

        Args:
            preview_limit: Maximum number of files to include in the preview

        Returns:
            tuple: (file_preview_list, total_file_count)
        """

    @property
    def file_count(self):
        """
        Get the total number of files in the dataset.
        For BATCH datasets, uses GCP API to count files.
        For other types, counts DatasetFile objects.

        Returns:
            int: Total number of files in the dataset
        """

    @property
    def total_file_size(self):
        """
        Get the total size of all files in the dataset in bytes.
        For BATCH datasets, uses GCP API to sum file sizes.
        For other types, sums DatasetFile sizes.

        Returns:
            int: Total size of all files in bytes
        """

    @property
    def all_files(self):
        """
        Get all files in the dataset.
        For BATCH datasets, uses GCP API to retrieve file information.
        For other types, returns DatasetFile objects formatted as dictionaries.

        Returns:
            list: List of dictionaries containing file information
        """


class DatasetFile(models.Model):
    """
    Model representing individual files within a dataset.
    """


class DatasetProjectAssignment(models.Model):
    """
    Through model for Dataset-Project assignments.
    Handles the many-to-many relationship between datasets and their assigned projects,
    including Seqera data link tracking.
    """
