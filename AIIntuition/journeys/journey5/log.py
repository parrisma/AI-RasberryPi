from datetime import datetime
from AIIntuition.journeys.journey5.event import Event, FailureEvent


class Log:
    @classmethod
    def log_event(cls,
                  event: Event,
                  *argv) -> None:
        """
        Post a standard form log message to the current sink of the Log Class/
        :param event: The event type
        :param argv: The components of the message body - all must support conversion to string
        """
        print(cls.log_message(event, *argv))

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


if __name__ == "__main__":
    ve = ValueError()
    Log.log_event(FailureEvent(), 'Hello', 3142, 'World')
