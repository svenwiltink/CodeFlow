import unittest
from PyFlow.workflow import Workflow, State


class TestState(State):

    called = False

    def run(self):
        assert TestState.called is False
        TestState.called = True


class TestWorkFlow(unittest.TestCase):

    workflowFile = "tests/resources/workflow.json"

    def createWorkflow(self):
        return Workflow.loadFromFile(self.workflowFile)

    def test_name(self):
        workflow = self.createWorkflow()
        assert workflow.name == 'test'

    def test_run(self):
        workflow = self.createWorkflow()
        workflow.run()
        assert TestState.called is True
