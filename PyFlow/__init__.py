import logging

logger = logging.getLogger('PyFlow')
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)

logger.addHandler(sh)


logger.info('initializing PyFlow package')
