import unittest
from unittest.mock import patch
from PyFlow.workflow import Workflow, State


class TestState(State):

    def run(self):
        print("running teststate")


class TestWorkFlow(unittest.TestCase):

    workflow = Workflow.loadFromFile("tests/resources/workflow.json")

    def test_name(self):
        assert self.workflow.name == 'test'

    def test_run(self):
        workflow = self.workflow
        with patch('test_workflow.TestState') as MockClass:
            instance = MockClass.return_value
            workflow.run()
            instance.run.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

