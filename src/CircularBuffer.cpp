
#include <new>
#include <iostream>

#include <string.h>

#include "CircularBuffer.h"

using namespace std;


CircularBuffer::CircularBuffer(size_t len) : m_capacity(len)
{
    m_buf_ptr = new uint8_t[len];
    m_read_ptr = m_buf_ptr;
    m_write_ptr = m_buf_ptr;
    m_len = 0;
}

void CircularBuffer::print(std::ostream& os)
{
    lock_guard<mutex> lock(m_mutex);

    cout << string("m_capacity:  ") << m_capacity << endl;
    os << string("m_len:       ") << m_len << endl;
    os << string("m_buf_ptr:   ") << static_cast<void*>(m_buf_ptr) << endl;
    os << string("m_read_ptr:  ") << static_cast<void*>(m_read_ptr) << endl;
    os << string("m_write_ptr: ") << static_cast<void*>(m_write_ptr) << endl;
}

/*
  
  case 1:
           
  |X|X| | | | | | | | | | |X|X|X|X|X|
      ^                   ^
      w                   r
 
  case 2:
 
  | | |X|X|X|X|X|X|X|X|X|X| | | | | |
      ^                   ^
      r                   w
 
*/


const int CircularBuffer::read(uint8_t *buf, const size_t len)
{
    uint8_t *buf_ptr = buf;
    size_t buf_len = len;

    size_t total_read = 0;
    size_t cpy_len;

    lock_guard<mutex> lock(m_mutex);

    while (buf_len > 0 && m_len > 0) {
        
        // case 1
        if (m_write_ptr <= m_read_ptr) {
            cpy_len = m_buf_ptr + m_capacity - m_read_ptr;
        }

        // case 2
        else if (m_write_ptr > m_read_ptr) {
            cpy_len = m_write_ptr - m_read_ptr;
        }

        if (buf_len < cpy_len) {
            cpy_len = buf_len;
        }

        memcpy(buf_ptr, m_read_ptr, cpy_len);

        buf_ptr += cpy_len;
        buf_len -= cpy_len;
        m_len -= cpy_len;
        total_read += cpy_len;
        m_read_ptr += cpy_len;

        // wrap m_read_ptr?
        if (m_read_ptr == (m_buf_ptr + m_capacity)) {
            m_read_ptr = m_buf_ptr;
        }
    }

    return total_read;
}
    

const int CircularBuffer::write(const uint8_t *buf, const size_t len)
{
    size_t buf_len = len;
    size_t buf_offset = 0;

    size_t total_written = 0;
    size_t cpy_len;

    lock_guard<mutex> lock(m_mutex);
    
    while (buf_len > 0 && m_len < m_capacity) {
           
        // case 1
        if (m_write_ptr < m_read_ptr) {
            cpy_len = m_read_ptr - m_write_ptr;
        }

        // case 2
        else {
            cpy_len = m_buf_ptr + m_capacity - m_write_ptr;
        }
        
        if (buf_len < cpy_len) {
            cpy_len = buf_len;
        }

        memcpy(m_write_ptr, buf + buf_offset, cpy_len);
        buf_offset += cpy_len;
        buf_len -= cpy_len;
        m_len += cpy_len;
        total_written += cpy_len;
        m_write_ptr += cpy_len;

        // wrap m_write_ptr?
        if (m_write_ptr == (m_buf_ptr + m_capacity)) {
            m_write_ptr = m_buf_ptr;
        }
    }

    return total_written;
}

CircularBuffer::~CircularBuffer()
{
    delete[] m_buf_ptr;
}
