import logging

class Logger:
    """Logger class for configuring and retrieving a logger instance."""

    def __init__(self, name: str):
        """Initialize the Logger with a given name and configure the logger."""
        self.logger = self._configure_logger(name)

    @staticmethod
    def _configure_logger(name: str) -> logging.Logger:
        """Configure the logger with the given name and return the logger instance."""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Stream handler for console output
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            # File handler for logging to a file
            file_handler = logging.FileHandler('robot.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def get_logger(self) -> logging.Logger:
        """Return the configured logger instance."""
        return self.logger
