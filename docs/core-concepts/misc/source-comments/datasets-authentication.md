
class PubSubAuthentication:
    """
    Custom authentication class for PubSub push notifications.
    Verifies the JWT token from the PubSub push request.
    In local development (API_BASE_URL is http://localhost:8000), authentication is skipped.
    """

    def authenticate(self, request):
        # Skip authentication in local development

        # Get the Cloud Pub/Sub-generated JWT in the "Authorization" header

            # Verify and decode the JWT. `verify_oauth2_token` verifies
            # the JWT signature, the `aud` claim, and the `exp` claim.

            # Validate claim details not covered by signature and audience verification

            # Ensure the email matches the expected service account

             # Return None for user since this is a service account
