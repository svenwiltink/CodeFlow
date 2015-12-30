import logging
import random

from PyFlow.workflow import Workflow, State

logger = logging.getLogger('PyFlow')
logger.setLevel(logging.INFO)

logger.info('starting example')


# list of state classes
class TestState(State):
    def run(self):
        self.variables['success'] = bool(random.getrandbits(1))


class DoMagicState(State):
    def run(self):
        print("gotta love this magic")


class PrintResultState(State):
    def run(self):
        print("success: {}".format(self.variables['success']))

# actually load and run the workflow
workflow = Workflow.loadFromFile('example/workflow.json')
workflow.run()
