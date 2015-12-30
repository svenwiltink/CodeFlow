import logging
import argparse
import json

from PyFlow.workflow import Workflow

logger = logging.getLogger('PyFlow')

logger.info('starting PyFlow')
logger.debug('parsing arguments')

parser = argparse.ArgumentParser(description='Runs a PyFlow')
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename) as workflowFile:
    logger.debug("file {} found".format(args.filename))
    contents = workflowFile.read()

    json_contents = json.loads(contents)
    logger.debug("json {}".format(json_contents))

    workflow = Workflow.loadFromJson(json_contents)
    logger.debug('returned instance {}'.format(workflow))
    workflow.run()


