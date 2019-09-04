class ApiError(Exception):
    """Base error class for the API"""


class ScriptDisabledError(ApiError):
    """
    Raised when a Script has been disabled on the server.
    """

    def __init__(self):
        super().__init__(f"Script is disabled on the server")


class TokenInvalidError(ApiError):
    """
    Raised when the given token is invalid.
    """

    def __init__(self):
        super().__init__(f"Script token is invalid")


class RateLimitError(ApiError):
    """
    Raised when a script's rate limit is reached.
    ".reset_after" is the time until the rate limit is completely reset
    ".retry_after" is the time until you can make another request
    ".server_errors" returns the errors field from the query
    """

    def __init__(self, reset_after, retry_after, errors):
        self.reset_after = reset_after
        self.retry_after = retry_after
        self.server_errors = errors
        super().__init__(f"Rate limit exceeded: {errors}")


class QueryError(ApiError):
    """
    Raised when a query fails with an non-null "error" field.
    ".request" is the raw request
    ".server_errors" returns the errors field from the query
    """

    def __init__(self, request, errors):
        self.request = request
        self.server_errors = errors
        super().__init__(f"Server failed to process the query: {errors}")


class MutationError(ApiError):
    """
    Raised when a mutation "success" field returns False.
    ".request" contains the request object.
    """

    def __init__(self, request):
        self.request = request
        super().__init__(f"{request['notice']}: {request['errors']}")


class UnknownObjectError(ApiError):
    """
    Raised when a query for a single item returns a null (nothing found).
    ".object" is the type of object being retrieved.
    ".id" is the ID used to retrieve it.
    ".name" is the name used to retrieve it.
    ".parent" is the parent object it should be on, "None" if it has no parent.
    """

    def __init__(self, object: str, id=None, name=None, parent=None):
        self.object = object
        self.id = id
        self.name = name
        self.parent = parent
        if id:
            message = f'No "{object}" found with id "{id}"'
        else:
            message = f'No "{object}" found with name "{name}"'
        if parent:
            message += f' under parent "{parent}"'
        super().__init__(message)
