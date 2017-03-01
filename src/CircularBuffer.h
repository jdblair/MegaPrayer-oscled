
#ifndef CIRCULAR_BUFFER_H
#define CIRCULAR_BUFFER_H

#include <stdint.h>
#include <strings.h>

#include <mutex>
#include <memory>

class CircularBuffer
{
 public:
    CircularBuffer(size_t len);
    int read(uint8_t *buf, size_t len);
    int write(uint8_t *buf, size_t len);
    ~CircularBuffer();

 private:
    size_t m_buf_len;

    uint8_t *m_buf_ptr;
    uint8_t *m_read_ptr;
    uint8_t *m_write_ptr;
    bool m_full;

    size_t m_len;

    std::mutex m_mutex;
};


#endif /* CIRCULAR_BUFFER_H */
