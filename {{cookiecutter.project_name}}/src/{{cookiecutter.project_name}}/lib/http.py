import json
from typing import cast

from django.http import JsonResponse as BaseJsonResponse

from {{cookiecutter.project_name}}.lib.types import JSONType


class JsonResponse(BaseJsonResponse):
    @property
    def data(self) -> JSONType:
        if self.content:
            return cast(JSONType, json.loads(self.content))
        return None
