import abc

from questcdncrawl.util.exceptions import UnknownAgentNameException


class QCDNCrawlerFactory(metaclass=abc.ABCMeta):
    crawler_registry = {}

    def __init__(self) -> None:
        super().__init__()

    def find_crawler(self, agent_name: str):
        if agent_name in self.crawler_registry:
            return self.crawler_registry.get(agent_name)
        else:
            raise UnknownAgentNameException(f'Agent {agent_name} does not have a registered crawler')
