import logging
import colorlog


class Logger(logging.Logger):
    def __init__(self, name='root', level=logging.NOTSET):
        super().__init__(name, level)
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # 设置日志格式
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)s:%(message)s [%(filename)s:%(lineno)d]",
            datefmt="%Y-%m-%d %H:%M:%S", log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            })
        console_handler.setFormatter(formatter)
        # 将处理器添加到日志记录器
        self.addHandler(console_handler)


if __name__ == '__main__':
    logger = Logger()
    logger.info("Hi edge")
