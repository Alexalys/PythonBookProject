from pydantic import BaseModel


class AbstractError(Exception):
    http_code: int = 500
    message: str = ""


class LlmError(AbstractError):
    def __str__(self):
        return f"Error occured in llm request. Details : {self.message}"
