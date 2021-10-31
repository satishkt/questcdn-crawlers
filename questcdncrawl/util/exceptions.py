class QCDNCrawlerException(BaseException):
    def __init__(self, message):
        super().__init__(message)


class UnknownAgentNameException(QCDNCrawlerException):
    def __init__(self, message):
        self.message = message
        super(UnknownAgentNameException, self).__init__(message)

    def __str__(self):
        return self.message
