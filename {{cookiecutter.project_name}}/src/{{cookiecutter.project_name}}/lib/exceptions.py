from typing import Any


class ValidationError(AssertionError):
    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message)
        if notes := kwargs.pop("notes", []):
            self.__notes__ = notes
        for key, value in kwargs.items():
            self.add_note(f"{key}: {value}")
