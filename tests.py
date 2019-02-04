import traceback
import unittest


def checkDependencies():
    print("\nChecking project dependencies..")

    print("checking matplotlib..")
    import matplotlib
    print("checked!")

    print("checking pandas..")
    import pandas
    print("checked!")

    print("checking numpy..")
    import numpy
    print("checked!")

    print("checking typing..")
    import typing
    print("checked!")
    print("All dependencies exists!")


def runUnittests():
    testmodules = [
        "test.brick_test", "test.collection_test", "test.ge_utils_test",
        "test.layout_test"
    ]

    suite = unittest.TestSuite()

    for t in testmodules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(t, globals(), locals(), ["suite"])
            suitefunction = getattr(mod, "suite")
            suite.addTest(suitefunction())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

    unittest.TextTestRunner().run(suite)


# Run the program
if __name__ == "__main__":
    try:
        checkDependencies()
        runUnittests()
    except SystemExit:
        pass
    except Exception as e:
        print("Some error occurred during the running! Process aborted..")
        print("\nError:", str(e))
        traceback.print_tb(e.__traceback__)
