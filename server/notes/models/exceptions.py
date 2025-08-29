class UnauthorizedAccessError(Exception):
    """Exception raised when a user tries to access a note they don't own."""
    pass
