import logging

logger = logging.getLogger('PyFlow')


class Workflow(object):

    name = None
    variables = {}
    currentStateName = "start"
    states = {}

    @staticmethod
    def loadFromJson(json):
        logger.debug('loading PyFlow from json')
        name = json['name']
        logger.debug('found name {}'.format(name))

        states = json['states']

        instance = Workflow()
        instance.name = name
        instance.states = states

        return instance

    def run(self):
        logger.info('running workflow {}'.format(self.name))
        logger.debug('current state {}'.format(self.currentStateName))

        state = self.states[self.currentStateName]
        while state is not None:
            nextState = self.handleState(state)
            logger.debug('next state: {}'.format(nextState))
            if nextState == 'finish' :
                break
            state = self.states[nextState]

        logger.debug('variables: {}'.format(self.variables))
        logger.info("workflow {} is finished")

    def handleState(self, state):
        type = state['type']
        if type == "empty":
            nextState = state['next']
            return nextState

        if type == 'run':
            packageName = state['package']
            className = state['class']

            mod = __import__(packageName, fromlist=[className])
            stateClass = getattr(mod, className)
            stateObject = stateClass()

            if isinstance(stateObject, State) :
                stateObject.variables = self.variables
                stateObject.run()
                self.variables = stateObject.variables
                nextState = state['next']
                return nextState
            else:
                raise RuntimeError("State {} from module {} is not a state object".format(className, packageName))


class State(object):

    name = None
    variables = {}

    def run(self):
        raise RuntimeError("run function not implemented")


class TestState(State):

    name = "test"

    def run(self):
        logger.debug("running the test state")
        self.variables['test'] = "fuck yes"




