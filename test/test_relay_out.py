import sys
from unittest import TestCase
from unittest import mock

sys.modules["znc"] = mock.MagicMock()

from relay_out import _contains_required_args, _parse_args, _is_valid_module_args


class Test_relay_out(TestCase):

    _TEST_ARGS = "--test0=zero --test1=one --test2=two"
    _TEST_REQUIRED_ARGS = ["--test0", "--test1", "--test2"]

    def test_contains_required_args(self):
        self.assertTrue(_contains_required_args(Test_relay_out._TEST_ARGS, Test_relay_out._TEST_REQUIRED_ARGS))

    def test_not_contains_required_args(self):
        self.assertFalse(_contains_required_args(
            Test_relay_out._TEST_ARGS, Test_relay_out._TEST_REQUIRED_ARGS + ["--test3"]))

    def test_parse_args(self):
        test_module_args = _parse_args(Test_relay_out._TEST_ARGS, Test_relay_out._TEST_REQUIRED_ARGS)
        self.assertTrue(Test_relay_out._TEST_REQUIRED_ARGS.sort() == list(test_module_args.keys()).sort())

    def test_no_extra_parse_args(self):
        test_module_args = _parse_args(
            Test_relay_out._TEST_ARGS + " --test3=three", Test_relay_out._TEST_REQUIRED_ARGS)
        self.assertTrue(Test_relay_out._TEST_REQUIRED_ARGS.sort() == list(test_module_args.keys()).sort())

    def test_missing_parse_args(self):
        try:
            _parse_args(Test_relay_out._TEST_ARGS.replace("--test2", ""), Test_relay_out._TEST_REQUIRED_ARGS)
        except Exception as error:
            self.assertTrue(isinstance(error, ValueError))

    def test_is_valid_module_args(self):
        test_module_args = _parse_args(Test_relay_out._TEST_ARGS, Test_relay_out._TEST_REQUIRED_ARGS)
        self.assertTrue(_is_valid_module_args(test_module_args, Test_relay_out._TEST_REQUIRED_ARGS))

    def test_not_is_valid_module_args(self):
        bad_module_args = {
            "--test0": "zero",
            "--test1": "one",
            "--test3": "two",
        }
        self.assertFalse(_is_valid_module_args(bad_module_args, Test_relay_out._TEST_REQUIRED_ARGS))
