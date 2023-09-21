class NoFileUploadedError(Exception):
    def __init__(self, code: int = 31, message: str = "No File Was Uploaded!"):
        self.code = code
        self.message = message
        super().__init__(self.message)