from typing import Optional

from .BaseAppConfig import BaseAppConfig


class AppConfig(BaseAppConfig):
    """
    Config to initialize an embedchain custom `App` instance, with extra config options.
    """

    def __init__(
        self,
        log_level=None,
        id=None,
        collect_metrics: Optional[bool] = None,
    ):
        """
        :param log_level: Optional. (String) Debug level
        ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'].
        :param id: Optional. ID of the app. Document metadata will have this id.
        :param collect_metrics: Defaults to True. Send anonymous telemetry to improve embedchain.
        """
        super().__init__(
            log_level=log_level,
            embedding_fn=AppConfig.default_embedding_function(),
            id=id,
            collect_metrics=collect_metrics,
        )
