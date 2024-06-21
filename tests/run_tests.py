import unittest

loader = unittest.TestLoader()
tests = loader.discover(start_dir='.', pattern='test*.py')
testRunner = unittest.TextTestRunner()
testRunner.run(tests)
