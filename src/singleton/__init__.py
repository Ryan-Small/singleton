import logging


fmt = '[%(asctime)s] [%(levelname)s\t\t] %(name)s: %(message)s'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

f_handler = logging.FileHandler('../agent.log')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
