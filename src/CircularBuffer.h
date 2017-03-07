
#ifndef CIRCULAR_BUFFER_H
#define CIRCULAR_BUFFER_H

#include <stdint.h>
#include <strings.h>

#include <mutex>
#include <memory>
#include <iostream>

class CircularBuffer
{
 public:
    CircularBuffer(size_t len);
    const int read(uint8_t *buf, const size_t len);
    const int write(const uint8_t *buf, const size_t len);
    void print(std::ostream& os);
    ~CircularBuffer();

 private:
    size_t m_capacity;

    uint8_t *m_buf_ptr;
    uint8_t *m_read_ptr;
    uint8_t *m_write_ptr;
    size_t m_len;

    std::mutex m_mutex;
};


#endif /* CIRCULAR_BUFFER_H */
