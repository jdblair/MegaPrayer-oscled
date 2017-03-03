
#include <string.h>
#include <thread>
#include <sys/time.h>

#include "CircularBuffer.h"
#include "Test_CircularBuffer.h"


CPPUNIT_TEST_SUITE_REGISTRATION(Test_CircularBuffer);


void Test_CircularBuffer::setUp(void)
{
}

void Test_CircularBuffer::tearDown(void)
{
}

void Test_CircularBuffer::test_readwrite(void)
{
    CircularBuffer c(16);

    char s[] = "abcdefghijklmnopqrstuvwxyz";
    uint8_t buf[128];

    size_t rc;

    /* test read of empty buffer */
    memset(buf, 0, 128);    
    rc = c.read(buf, 128);
    CPPUNIT_ASSERT_EQUAL((size_t)0, rc);

    /* test writing more than buffer size (aligned at start of m_buf)*/
    memset(buf, 0, 128);
    rc = c.write((uint8_t*)s, 26);
    CPPUNIT_ASSERT_EQUAL((size_t)16, rc);
    rc = c.read(buf, 128);
    CPPUNIT_ASSERT_EQUAL((size_t)16, rc);
    CPPUNIT_ASSERT_EQUAL(string("abcdefghijklmnop"), string((char*)buf));

    /* write 8 chars, read 4 chars */
    memset(buf, 0, 128);
    rc = c.write((uint8_t*)s, 8);
    CPPUNIT_ASSERT_EQUAL((size_t)8, rc);
    rc = c.read(buf, 4);
    CPPUNIT_ASSERT_EQUAL((size_t)4, rc);
    CPPUNIT_ASSERT_EQUAL(string("abcd"), string((char*)buf));

    /* write 8 chars, read 16 chars */
    memset(buf, 0, 128);
    rc = c.write((uint8_t*)s, 8);
    CPPUNIT_ASSERT_EQUAL((size_t)8, rc);
    rc = c.read(buf, 16);
    CPPUNIT_ASSERT_EQUAL((size_t)12, rc);
    CPPUNIT_ASSERT_EQUAL(string("efghabcdefgh"), string((char*)buf));

    /* write 8 chars, read 16 chars */
    memset(buf, 0, 128);
    rc = c.write((uint8_t*)s, 8);
    CPPUNIT_ASSERT_EQUAL((size_t)8, rc);
    rc = c.read(buf, 16);
    CPPUNIT_ASSERT_EQUAL((size_t)8, rc);
    CPPUNIT_ASSERT_EQUAL(string("abcdefgh"), string((char*)buf));

    /* test writing more than buffer size again (make sure wrapping works)*/
    memset(buf, 0, 128);
    rc = c.write((uint8_t*)s, 26);
    CPPUNIT_ASSERT_EQUAL((size_t)16, rc);
    rc = c.read(buf, 128);
    CPPUNIT_ASSERT_EQUAL((size_t)16, rc);
    CPPUNIT_ASSERT_EQUAL(string("abcdefghijklmnop"), string((char*)buf));

    /* write something, try zero length read */
    memset(buf, 0, 128);
    rc = c.write((uint8_t*)s, 4);
    CPPUNIT_ASSERT_EQUAL((size_t)4, rc);
    rc = c.read(buf, 0);
    CPPUNIT_ASSERT_EQUAL((size_t)0, rc);

    /* now empty the buffer again */
    memset(buf, 0, 128);
    rc = c.read(buf, 128);
    CPPUNIT_ASSERT_EQUAL((size_t)4, rc);
}


#define STRESS_TEST_COUNT 1024 * 512
void stress_test_write(CircularBuffer &c)
{
    int i;

    for (i = 0; i < STRESS_TEST_COUNT; i++) {
        while (c.write(reinterpret_cast<uint8_t*>(&i), static_cast<size_t>(sizeof(i))) != sizeof(i)) {}
    }
}

void stress_test_read(CircularBuffer &c)
{
    int i;
    int count = 0;

    while (i >= 0) {
        if (c.read(reinterpret_cast<uint8_t*>(&i), static_cast<size_t>(sizeof(i))) == 4) {
            ++count;
        }
    }

    CPPUNIT_ASSERT_EQUAL(STRESS_TEST_COUNT * 2 + 1, count);
    
}

void Test_CircularBuffer::stress_test(void)
{
    CircularBuffer c(1024);

    struct timeval time_start;
    struct timeval time_stop;

    gettimeofday(&time_start, NULL);
    printf("\nstress test start: %ld.%ld\n", time_start.tv_sec, time_start.tv_usec);
    
    thread t_write(stress_test_write, ref(c));
    thread t_write2(stress_test_write, ref(c));
    //thread t_write3(stress_test_write, ref(c));
    //thread t_write4(stress_test_write, ref(c));
    thread t_read(stress_test_read, ref(c));

    t_write.join();
    t_write2.join();
    //t_write3.join();
    //t_write4.join();

    // send -1 to signal to the read thread that we are done
    int i = -1;
    while (c.write(reinterpret_cast<uint8_t*>(&i), static_cast<size_t>(sizeof(i))) != sizeof(i)) {}

    t_read.join();

    gettimeofday(&time_stop, NULL);
    printf("stress test stop:  %ld.%ld\n", time_stop.tv_sec, time_stop.tv_usec);
    printf("run-time in seconds:    %ld\n", time_stop.tv_sec - time_start.tv_sec);
}
