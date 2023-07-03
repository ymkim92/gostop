import sys
import unittest
from io import StringIO

try:
    import mock
except ImportError:
    import unittest.mock as mock

from src.gostop.humanagent import HumanAgent


class HumanAgentTest(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    def test_get_action(self):
        agent = HumanAgent("Test Agent")
        with mock.patch("src.gostop.humanagent.input", return_value="0"):
            self.assertEqual(
                agent.get_action(None, ["Action1", "Action2", "Action3"]), "Action1"
            )
        with mock.patch("src.gostop.humanagent.input", side_effect=["3", "2"]):
            self.assertEqual(
                agent.get_action(None, ["Action1", "Action2", "Action3"]), "Action3"
            )
