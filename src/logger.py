import logging

class Logger:
    def __init__(self, name):
        self.logger = self.configure_logger(name)

    @staticmethod
    def configure_logger(name):

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            file_handler = logging.FileHandler('robot.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def get_logger(self):
        return self.logger