from uvicorn.workers import UvicornWorker as BaseUvicornWorker


class UvicornWorker(BaseUvicornWorker):
    @property
    def CONFIG_KWARGS(self):  # noqa: N802
        kwargs = super().CONFIG_KWARGS.copy()
        kwargs["lifespan"] = "off"
        return kwargs
