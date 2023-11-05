import unittest

test_loader = unittest.TestLoader()
test_suite = test_loader.discover("test")

test_runner = unittest.TextTestRunner()
result = test_runner.run(test_suite)

exit_code = 0 if result.wasSuccessful() else 1
exit(exit_code)
