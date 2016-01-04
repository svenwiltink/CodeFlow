import logging

logger = logging.getLogger('CodeFlow')
logger.setLevel(logging.WARNING)

sh = logging.StreamHandler()
sh.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)

logger.addHandler(sh)
