import logging
import argparse

from PyFlow.workflow import Workflow

logger = logging.getLogger('PyFlow')

logger.info('starting PyFlow')
logger.debug('parsing arguments')

parser = argparse.ArgumentParser(description='Runs a PyFlow')
parser.add_argument('filename')
args = parser.parse_args()

workflow = Workflow.loadFromFile(args.filename)
workflow.run()


