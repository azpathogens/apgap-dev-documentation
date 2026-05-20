class MoveJWTCookiesIntoTheBody(MiddlewareMixin):
    """
    for Django Rest Framework JWT endpoints --- check for tokens in the request.COOKIES and move them into the payload
    """

    def _is_token_endpoint(self, path):
        """Check if the path is a token endpoint (with or without trailing slash)."""
