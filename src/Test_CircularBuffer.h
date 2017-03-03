
#ifndef TEST_CIRCULARBUFFER_H
#define TEST_CIRCULARBUFFER_H

#include <cppunit/TestCase.h>
#include <cppunit/TestCaller.h>
#include <cppunit/extensions/HelperMacros.h>

using namespace std;
using namespace CPPUNIT_NS;

class Test_CircularBuffer : public CPPUNIT_NS::TestFixture {
public:
    void setUp(void);
    void tearDown(void);
    void test_readwrite(void);
    void stress_test(void);

    CPPUNIT_TEST_SUITE(Test_CircularBuffer);
    CPPUNIT_TEST(test_readwrite);
    CPPUNIT_TEST(stress_test);
    CPPUNIT_TEST_SUITE_END();

private:
};


#endif /* TEST_CIRCULARBUFFER_H */
