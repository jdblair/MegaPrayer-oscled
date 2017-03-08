
#include <iostream>

#include <cppunit/ui/text/TestRunner.h>
#include <cppunit/TestResult.h>
#include <cppunit/TestResultCollector.h>
#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/BriefTestProgressListener.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/TextOutputter.h>

using namespace std;
using namespace CPPUNIT_NS;

int main(int argc, char **argv)
{
    TextTestRunner runner;
    runner.addTest(TestFactoryRegistry::getRegistry().makeTest());

    bool wasSuccessful = runner.run("", false);  // run our tests
    return !wasSuccessful;
}
