
#include <new>


#include <string.h>

#include "CircularBuffer.h"

using namespace std;

#define BUFFER_EMPTY (m_read_ptr == m_write_ptr && ! m_full)

CircularBuffer::CircularBuffer(size_t len) : m_buf_len(len)
{
    m_buf_ptr = new uint8_t[len];
    m_read_ptr = m_buf_ptr;
    m_write_ptr = m_buf_ptr;
    m_full = false;
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


int CircularBuffer::read(uint8_t *buf, size_t len)
{
   uint8_t *buf_ptr = buf;
    size_t buf_len = len;

    size_t total_read = 0;
    size_t cpy_len;

    lock_guard<mutex> lock(m_mutex);

    while (buf_len > 0 && ! BUFFER_EMPTY) {
        
        // case 1
        if (m_write_ptr < m_read_ptr) {
            cpy_len = m_buf_ptr + m_buf_len - m_read_ptr;
        }

        // case 2
        else if (m_write_ptr > m_read_ptr) {
            cpy_len = m_write_ptr - m_read_ptr;
        }

        // buffer is full
        else if (m_full) {
            cpy_len = m_buf_len;
        }

        if (buf_len < cpy_len) {
            cpy_len = buf_len;
        }

        memcpy(buf_ptr, m_read_ptr, cpy_len);

        buf_ptr += cpy_len;
        buf_len -= cpy_len;
        total_read += cpy_len;
        m_read_ptr += cpy_len;

        // wrap m_read_ptr?
        if (m_read_ptr == (m_buf_ptr + m_buf_len)) {
            m_read_ptr = m_buf_ptr;
        }

        if (total_read > 0) {
            m_full = false;
        }
    }

    return total_read;
}
    

int CircularBuffer::write(uint8_t *buf, size_t len)
{
    uint8_t *buf_ptr = buf;
    size_t buf_len = len;

    size_t total_written = 0;
    size_t cpy_len;

    lock_guard<mutex> lock(m_mutex);
    
    while (buf_len > 0 && ! m_full) {
           
        // case 1
        if (m_write_ptr < m_read_ptr) {
            cpy_len = m_read_ptr - m_write_ptr;
        }

        // case 2
        else {
            cpy_len = m_buf_ptr + m_buf_len - m_write_ptr;
        }
        
        if (buf_len < cpy_len) {
            cpy_len = buf_len;
        }

        memcpy(m_write_ptr, buf_ptr, cpy_len);
        buf_ptr += cpy_len;
        buf_len -= cpy_len;
        total_written += cpy_len;
        m_write_ptr += cpy_len;

        // wrap m_write_ptr?
        if (m_write_ptr == (m_buf_ptr + m_buf_len)) {
            m_write_ptr = m_buf_ptr;
        }

        if (m_write_ptr == m_read_ptr) {
            m_full = true;
        }
    }

    return total_written;
}

CircularBuffer::~CircularBuffer()
{
    delete[] m_buf_ptr;
}
