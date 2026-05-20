
class Upload(models.Model):
    @property
    def full_target_path(self):
        # For batch uploads, use the File's filename (which may be a unique name)
        # since that's where the file will actually be stored.
        # Upload.filename contains the original name for source blob lookup.


class BatchUpload(models.Model):

    @property
    def expires_at(self) -> datetime:
        """
        Calculate the expiration datetime based on created_at and time_to_live.

        Returns:
            datetime: The expiration datetime
        """

    @property
    def is_expired(self) -> bool:
        """
        Check if the batch upload has expired.

        Returns:
            bool: True if expired, False otherwise
        """

    @property
    def batch_sa_key(self) -> dict:
        """
        Get the batch service account key JSON from GCP Secret Manager.
        The secret is stored in the project's GCP project and named according to
        the format stored in batch_service_account_secret_name.

        Returns:
            dict: The service account key as a dictionary, or empty dict if not found
        """
