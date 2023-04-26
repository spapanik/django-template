from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class BaseView(View):
    template_name: str

    @staticmethod
    async def get_context_data(**kwargs: Any) -> dict[str, Any]:
        return kwargs

    async def get_template_name(self, **_kwargs: Any) -> str:
        return self.template_name

    async def render(self, context: dict[str, Any]) -> HttpResponse:
        template = await self.get_template_name(**context)
        return render(self.request, template, context)

    async def get(
        self, request: HttpRequest, *_args: Any, **kwargs: Any  # noqa: ARG002
    ) -> HttpResponse:
        context = await self.get_context_data(**kwargs)
        return await self.render(context)
