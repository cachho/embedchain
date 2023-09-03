import os
import unittest
from unittest.mock import patch

from embedchain import App
from embedchain.config import AppConfig
from embedchain.llm.base_llm import BaseLlm


class TestApp(unittest.TestCase):
    def setUp(self):
        os.environ["OPENAI_API_KEY"] = "test_key"
        self.app = App(config=AppConfig(collect_metrics=False))

    @patch.object(App, "retrieve_from_database", return_value=["Test context"])
    @patch.object(BaseLlm, "get_answer_from_llm", return_value="Test answer")
    def test_chat_with_memory(self, mock_get_answer, mock_retrieve):
        """
        This test checks the functionality of the 'chat' method in the App class with respect to the chat history
        memory.
        The 'chat' method is called twice. The first call initializes the chat history memory.
        The second call is expected to use the chat history from the first call.

        Key assumptions tested:
            called with correct arguments, adding the correct chat history.
        - After the first call, 'memory.chat_memory.add_user_message' and 'memory.chat_memory.add_ai_message' are
        - During the second call, the 'chat' method uses the chat history from the first call.

        The test isolates the 'chat' method behavior by mocking out 'retrieve_from_database', 'get_answer_from_llm' and
        'memory' methods.
        """
        app = App()
        first_answer = app.chat("Test query 1")
        self.assertEqual(first_answer, "Test answer")
        self.assertEqual(len(app.llm.memory.chat_memory.messages), 2)
        self.assertEqual(len(app.llm.history.splitlines()), 2)
        second_answer = app.chat("Test query 2")
        self.assertEqual(second_answer, "Test answer")
        self.assertEqual(len(app.llm.memory.chat_memory.messages), 4)
        self.assertEqual(len(app.llm.history.splitlines()), 4)

    @patch.object(App, "retrieve_from_database", return_value=["Test context"])
    @patch.object(BaseLlm, "get_answer_from_llm", return_value="Test answer")
    def test_template_replacement(self, mock_get_answer, mock_retrieve):
        """
        Tests that if a default template is used and it doesn't contain history,
        the default template is swapped in.

        Also tests that a dry run does not change the history
        """
        app = App()
        first_answer = app.chat("Test query 1")
        self.assertEqual(first_answer, "Test answer")
        self.assertEqual(len(app.llm.history.splitlines()), 2)
        history = app.llm.history
        dry_run = app.chat("Test query 2", dry_run=True)
        self.assertIn("History:", dry_run)
        self.assertEqual(history, app.llm.history)
        self.assertEqual(len(app.llm.history.splitlines()), 2)