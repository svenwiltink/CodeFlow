import unittest
import sys
from CodeFlow.workflow import Workflow, State


ispython3 = False
if sys.version_info > (3, 0):
    ispython3 = True


class TestState(State):

    called = False

    def run(self):
        assert TestState.called is False
        TestState.called = True


class NotAState:

    def run(self):
        pass


class NoRunMethodState(State):
    pass


class TriggerTrueState(State):

    called = False

    def run(self):
        assert TriggerTrueState.called is False
        TriggerTrueState.called = True


class TriggerFalseState(State):

    called = False

    def run(self):
        assert TriggerFalseState.called is False
        TriggerFalseState.called = True


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

    def test_is_not_state(self):
        workflow = Workflow.loadFromFile("tests/resources/not_a_state_workflow.json")
        with self.assertRaises(TypeError):
            workflow.run()

    def test_no_run_method(self):
        workflow = Workflow.loadFromFile("tests/resources/no_run_method_state_workflow.json")
        if ispython3:
            with self.assertRaisesRegex(RuntimeError, "run function not implemented"):
                workflow.run()
        else:
            with self.assertRaisesRegexp(RuntimeError, "run function not implemented"):
                workflow.run()

    def test_unknown_state_type(self):
        workflow = Workflow.loadFromFile('tests/resources/unknown_type_workflow.json')
        if ispython3:
            with self.assertRaisesRegex(RuntimeError, "Unknown state type .*"):
                workflow.run()
        else:
            with self.assertRaisesRegexp(RuntimeError, "Unknown state type .*"):
                workflow.run()

    def test_trigger_true(self):
        workflow = Workflow.loadFromFile('tests/resources/trigger_workflow.json')
        workflow.variables['success'] = True

        TriggerTrueState.called = False
        TriggerFalseState.called = False

        workflow.run()

        assert TriggerTrueState.called is True
        assert TriggerFalseState.called is False

    def test_trigger_default(self):
        workflow = Workflow.loadFromFile('tests/resources/trigger_workflow.json')
        workflow.variables['success'] = False

        TriggerTrueState.called = False
        TriggerFalseState.called = False

        workflow.run()

        assert TriggerTrueState.called is False
        assert TriggerFalseState.called is True

    def test_trigger_multiple(self):
        workflow = Workflow.loadFromFile('tests/resources/trigger_multiple_workflow.json')
        workflow.variables['success'] = True

        if ispython3:
            with self.assertRaisesRegex(RuntimeError, "A workflow could transition to multiple states"):
                workflow.run()
        else:
            with self.assertRaisesRegexp(RuntimeError, "A workflow could transition to multiple states"):
                workflow.run()

    def test_trigger_multiple_same(self):
        workflow = Workflow.loadFromFile('tests/resources/trigger_multiple_same_workflow.json')
        workflow.variables['success'] = True

        TriggerTrueState.called = False
        TriggerFalseState.called = False
        workflow.run()

        assert TriggerTrueState.called is True
        assert TriggerFalseState.called is False

    def test_trigger_recursive_variable(self):
        workflow = Workflow.loadFromFile('tests/resources/trigger_recursive_variable_workflow.json')
        workflow.variables['recursive'] = {'variable': {'check': True}}

        TriggerTrueState.called = False
        TriggerFalseState.called = False
        workflow.run()

        assert TriggerTrueState.called is True
        assert TriggerFalseState.called is False

    def test_trigger_recursive_unset(self):
        workflow = Workflow.loadFromFile('tests/resources/trigger_recursive_variable_workflow.json')
        workflow.variables['success'] = True

        TriggerTrueState.called = False
        TriggerFalseState.called = False
        workflow.run()

        assert TriggerTrueState.called is False
        assert TriggerFalseState.called is True

    def test_trigger_recursive_empty(self):
        workflow = Workflow.loadFromFile('tests/resources/trigger_recursive_variable_none_workflow.json')
        workflow.variables['recursive'] = {'variable': {'check': None}}

        assert workflow.variables['recursive']['variable']['check'] is None
        TriggerTrueState.called = False
        TriggerFalseState.called = False
        workflow.run()

        assert TriggerTrueState.called is True
        assert TriggerFalseState.called is False
