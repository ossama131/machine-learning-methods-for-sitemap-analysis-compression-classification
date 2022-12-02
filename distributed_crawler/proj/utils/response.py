class Response:
    pass

class SucessfulResponse(Response):
    __slots__ = 'content'
    
    def __init__(self, content) -> None:
        super().__init__()
        self.content = content

class FailedResponse(Response):
    pass
