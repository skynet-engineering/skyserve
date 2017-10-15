import time


class LogLevel:
    """
    Mapping of log level enums to names.
    """
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'


class Logger:
    def __init__(self, name):
        """
        Initializes a logger.

        :param name: Name to attach to every log entry generated with this logger.
        """
        self.name = name

    def debug(self, message):
        """
        Log a debug message.

        :param message: Message to log.
        """
        return self._print_log(LogLevel.DEBUG, message)

    def info(self, message):
        """
        Log an info message.

        :param message: Message to log.
        """
        return self._print_log(LogLevel.INFO, message)

    def warn(self, message):
        """
        Log a warning message.

        :param message: Message to log.
        """
        return self._print_log(LogLevel.WARN, message)

    def error(self, message):
        """
        Log an error message.

        :param message: Message to log.
        """
        return self._print_log(LogLevel.ERROR, message)

    def _print_log(self, level, message):
        """
        Print a log entry to standard output, with the timestamp, log level, and context name
        automatically prefixed.

        :param level: Target log level.
        :param message: Message to log.
        """
        hms = time.strftime('%H:%M:%S')
        self._print_stdout(
            '[{hms}] [{name}] [{level}] {message}'.format(
                hms=hms,
                name=self.name,
                level=level,
                message=message,
            )
        )

    @staticmethod
    def _print_stdout(line):
        """
        Print a line to standard output.

        :param line: Line to print.
        """
        print line
