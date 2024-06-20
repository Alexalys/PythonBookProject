class AbstractException(Exception):
    http_code: int = 500
    message: str = ""


class LlmException(AbstractException):
    def __str__(self):
        return f"Error occured in llm request. Details : {self.message}"


class DBException(AbstractException):
    def __str__(self):
        return f"Error occured in db query. Details : {self.message}"
