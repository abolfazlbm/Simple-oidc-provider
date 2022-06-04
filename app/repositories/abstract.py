class Status:
    """
    Status of the repository
    """
    OK = 0
    ERROR = 1
    WARNING = 2

    def __init__(self, status, message, code=None, http_code=None, data=None):
        self.status = status
        self.message = message
        self.code = code
        self.http_code = http_code
        self.data = data
