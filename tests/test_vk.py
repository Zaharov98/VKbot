import unittest

import vk


class VKStreamingApiRulesTest(unittest.TestCase):
    """Testing connection to vk streaming api"""

    def setUp(self):
        self._stream = vk.get_server_streaming_key()

    def test_rule_add_del(self):
        """adding rule 'python' """
        self.assertEqual(vk.set_rule(self._stream, "python", 12), "rule python added!")
        self.assertIn({"tag": "12", "value": "python"}, vk.get_rules(self._stream))
        self.assertEqual(vk.delete_rule(self._stream, 12), "rule 12 deleted!")

    @unittest.skip
    @unittest.expectedFailure
    def test_listen_server(self):
        """no exceptions during listening vk stream"""
        self.assertRaises(vk.listen_stream(self._stream))

if __name__ == "__main__":
    unittest.main()


