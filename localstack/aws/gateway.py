import logging
from typing import List

from localstack.http import Request, Response

from .api import RequestContext
from .chain import ExceptionHandler, Handler, HandlerChain

LOG = logging.getLogger(__name__)


class Gateway:
    """
    A gateway creates new HandlerChain instances for each request and processes requests through them.
    """

    request_handlers: List[Handler]
    response_handlers: List[Handler]
    exception_handlers: List[ExceptionHandler]

    def __init__(self) -> None:
        super().__init__()
        self.request_handlers = list()
        self.response_handlers = list()
        self.exception_handlers = list()

    def handle(self, context: RequestContext, response: Response) -> None:
        """Exposes the same interface as ``HandlerChain.handle``."""
        return self.new_chain().handle(context, response)

    def new_chain(self) -> HandlerChain:
        return HandlerChain(self.request_handlers, self.response_handlers, self.exception_handlers)

    def process(self, request: Request, response: Response):
        context = RequestContext()
        context.request = request
        self.handle(context, response)
