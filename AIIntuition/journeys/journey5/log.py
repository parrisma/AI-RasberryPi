import uuid
from datetime import datetime
from AIIntuition.journeys.journey5.event import Event, FailureEvent


class Log:
    _file_handle = None

    @classmethod
    def log_event(cls,
                  event: Event,
                  *argv) -> None:
        """
        Post a standard form log message to the current sink of the Log Class/
        :param event: The event type
        :param argv: The components of the message body - all must support conversion to string
        """
        log_msg = cls.log_message(event, *argv)
        print(log_msg)
        cls._log_to_file(log_msg)

    @classmethod
    def log_message(cls,
                    event: Event,
                    *argv) -> str:
        """
        Return a standard form log message
        :param event: The event type
        :param argv: The components of the message body - all must support conversion to string
        :return: Standard form Log message - current time stamp, event type & message body
        """
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        log_message = ''.join((ts, ':', str(event), ':'))
        for arg in argv:
            log_message = ''.join((log_message, str(arg), ' '))
        return log_message

    @classmethod
    def _log_file_name(cls) -> str:
        return datetime.now().strftime('%Y-%m-%d-%H-%M-%S-') + uuid.uuid4().hex + '.log'

    @classmethod
    def _log_to_file(cls, log_msg: str) -> None:
        if cls._file_handle is None:
            cls._file_handle = open(cls._log_file_name(), "w")
        cls._file_handle.write(log_msg + '\n')
        return


if __name__ == "__main__":
    ve = ValueError()
    Log.log_event(FailureEvent(), 'Hello', 3142, 'World')
