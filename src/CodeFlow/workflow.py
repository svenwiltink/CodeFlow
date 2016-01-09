import logging
import json
import time
import subprocess

logger = logging.getLogger('CodeFlow')


class Workflow(object):

    name = None
    variables = {}
    states = {}

    @staticmethod
    def loadFromFile(filename):
        with open(filename) as workflowFile:
            contents = workflowFile.read()
            json_contents = json.loads(contents)
            return Workflow.loadFromJson(json_contents)

    @staticmethod
    def loadFromJson(json):
        logger.debug('loading PyFlow from json')
        name = json['name']

        states = json['states']

        instance = Workflow()
        instance.name = name
        instance.states = states
        instance.variables = {}

        return instance

    def run(self):
        logger.info('running workflow {}'.format(self.name))

        state = self.states["start"]
        while state is not None:
            nextState = self.handleState(state)
            logger.debug("next state {}".format(nextState))
            if nextState == 'finish':
                break
            state = self.states[nextState]

        logger.info("workflow {} is finished")

    def handleState(self, state):
        type = state['type']
        if type == "empty":
            nextState = state['next']
            return nextState

        elif type == 'run':
            packageName = state['package']
            className = state['class']

            mod = __import__(packageName, fromlist=[className])
            stateClass = getattr(mod, className)
            stateObject = stateClass()

            if isinstance(stateObject, State):
                stateObject.variables = self.variables
                stateObject.run()
                self.variables = stateObject.variables
                nextState = state['next']
                return nextState
            else:
                raise TypeError("State {} from module {} is not a state object".format(className, packageName))

        elif type == 'trigger':
            default = state['next']
            triggers = state['triggers']

            nextState = None
            for trigger in triggers:
                requiredValue = trigger['value']
                varNames = trigger['variableName']
                varNames = varNames.split(';')

                value = self.variables
                ignoreValue = False

                for varName in varNames:
                    if varName in value:
                        value = value.get(varName)
                    else:
                        ignoreValue = True
                        break

                if ignoreValue == False and value == requiredValue:
                    if nextState is not None and nextState != trigger['next']:
                        raise RuntimeError("A workflow could transition to multiple states")
                    nextState = trigger['next']

            if nextState is None:
                nextState = default

            return nextState

        elif type == 'sleep':
            nextState = state['next']
            time.sleep(state['sleepTime'])

            return nextState

        elif type == 'exec':
            nextState = state['next']
            subprocess.call(state['command'])

            return nextState

        else:
            raise RuntimeError("Unknown state type {}".format(type))


class State(object):

    variables = {}

    def run(self):
        raise RuntimeError("run function not implemented")
