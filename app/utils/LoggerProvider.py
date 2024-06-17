import logging
from logging.handlers import RotatingFileHandler

class LoggerProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, 
        log_file: str = "app.log", 
        max_bytes: int = 10485760, 
        backup_count: int = 10, 
        log_level: str = "INFO"
    ):
        """
        Initializes the LoggerProvider with specified configuration.

        Args:
            log_file (str): The log file path.
            max_bytes (int): The maximum size in bytes before the log file is rotated.
            backup_count (int): The number of backup files to keep.
            log_level (str): The logging level.
        """
        if not hasattr(self, 'initialized'):
            self.log_file = log_file
            self.max_bytes = max_bytes
            self.backup_count = backup_count
            self.log_level = log_level.upper()
            self.logger = self._setup_logger()
            self.initialized = True

    def _setup_logger(self) -> logging.Logger:
        """
        Sets up the logger with the specified handlers and formatters.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger("fastapi_logger")
        logger.setLevel(self._get_log_level(self.log_level))

        # Create handlers
        stream_handler = logging.StreamHandler()
        file_handler = RotatingFileHandler(
            self.log_file, 
            maxBytes=self.max_bytes, 
            backupCount=self.backup_count
        )

        # Set log level for handlers
        stream_handler.setLevel(self._get_log_level(self.log_level))
        file_handler.setLevel(self._get_log_level(self.log_level))

        # Create formatters and add to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        return logger

    def _get_log_level(self, level: str) -> int:
        """
        Maps a string log level to a logging module constant.

        Args:
            level (str): The log level as a string.

        Returns:
            int: The corresponding logging level constant.
        """
        return getattr(logging, level.upper(), logging.INFO)

    def set_level(self, level: str) -> None:
        """
        Sets the logging level for the logger and its handlers.

        Args:
            level (str): The log level to set.
        """
        log_level = self._get_log_level(level)
        self.logger.setLevel(log_level)
        for handler in self.logger.handlers:
            handler.setLevel(log_level)

    def get_logger(self) -> logging.Logger:
        """
        Gets the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger
