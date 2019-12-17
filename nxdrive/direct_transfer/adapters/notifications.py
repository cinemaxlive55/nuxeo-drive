import abc


class AbstractNotifications(abc.ABC):
    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError
