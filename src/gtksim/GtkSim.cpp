

#include <iostream>
#include <mutex>
#include <thread>
#include <goocanvas.h>
#include <math.h>

#include "GtkSim.hpp"

#include "stdlib.h"
#include "stdio.h"
#include "string.h"

using namespace std;


/* This is our handler for the "delete-event" signal of the window, which
   is emitted when the 'x' close button is clicked. We just exit here. */
static gboolean
on_delete_event (GtkWidget *window,
                 GdkEvent  *event,
                 gpointer   unused_data)
{
  exit (0);
}


GtkSim::GtkSim() {
    m_gtk_ready = false;
    
    // initialize m_leds
    for (int i = 0; i < BEAD_COUNT; i++) {
        led_t led(0,0,0);
        m_leds.push_back(led);
    }

    //m_bead_values = g_value_array_new(BEAD_COUNT);
    for (int i = 0; i < BEAD_COUNT; i++) {
        g_value_init(&m_bead_values[i], G_TYPE_STRING);
    }
    thread t_gtkmain = thread(&GtkSim::main, this);
    t_gtkmain.detach();
};


// shared_ptr<GtkSim::Serial> GtkSim::newSerial(int low, int high, bool reversed) {
//     shared_ptr<GtkSim::Serial> ser(new GtkSim::Serial(low, high, reversed));
//     return ser;
// }

// this simulates the LED modules by reading the values and setting the vector "beads"
// this is not a true simulation - it depends on the upper layer performing
// a single update in a single send() operation. since this is how I wrote the code
// it should work. however, a more correct simulation would need to simulate timing,
// since the LED modules reset after a 500 usec delay.
void GtkSimSerial::send(unsigned char *buf, size_t len) {
    // most of the time there is no change to buf
    // this check avoids calling the gtk machinery if there has been no change
    if (len > m_last_buf_len) {
        m_last_buf = static_cast<unsigned char *>(realloc(m_last_buf, len));
        m_last_buf_len = len;
    }

    bool buf_changed = false;
    for (int i = 0; i < len; i++) {
        if (m_last_buf[i] != buf[i]) {
            buf_changed = true;
            break;
        }
    }

    if (buf_changed) {
        memcpy(m_last_buf, buf, len);
    } else {
        return;
    }

    // end buffer changed check

    size_t buf_len(len);
    size_t led_range = m_led_high - m_led_low + 1;

    if (buf_len > led_range * 3) {
        buf_len = led_range * 3;
    }

    // cout << "led_range: " << led_range << endl;
    // cout << "buf_len: " << buf_len << endl;

    int i = 0;
    int led_num = m_led_reversed ? m_led_high : m_led_low;

    for (i = 0; i < buf_len; i+=3) {
        cout << "led_num: " << led_num << endl;
        m_sim->m_leds.at(led_num) = led_t(buf[i], buf[i+1], buf[i+2]);
        led_num = m_led_reversed ? led_num - 1 : led_num + 1;
    }

    if (m_sim->m_gtk_ready)
        gtk_idle_add_priority(G_PRIORITY_DEFAULT_IDLE, gtksim_update_beads, m_sim.get());
}


gboolean gtksim_update_beads(gpointer user_data)
{
    GtkSim *sim = static_cast<GtkSim*>(user_data);
    sim->update_beads();

    return false;
}

//gboolean gtksim_update_beads(gpointer user_data)
void GtkSim::update_beads()
{
    if (! m_gtk_ready)
        return;

    char color[16];
    for (int i = 0; i < GtkSim::BEAD_COUNT; i++) {
        sprintf(color, "#%02x%02x%02x",
                static_cast<unsigned int>(m_leds.at(i).r),
                static_cast<unsigned int>(m_leds.at(i).g),
                static_cast<unsigned int>(m_leds.at(i).b));
        g_value_set_string(&m_bead_values[i], color);
        g_object_set_property(G_OBJECT(g_beads[i]), "fill-color", &m_bead_values[i]);
    }
}

void GtkSim::start()
{
}

void GtkSim::main()
{
    GtkWidget *window, *scrolled_win, *canvas;
    GooCanvasItem *root, *rect_item, *text_item;

    /* Initialize GTK+. */
    gtk_set_locale ();
    //gtk_init (&argc, &argv);
    gtk_init (NULL, NULL);

    /* Create the window and widgets. */
    window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    gtk_window_set_default_size (GTK_WINDOW (window), 640, 600);
    gtk_widget_show (window);
    g_signal_connect (window, "delete_event", (GtkSignalFunc) on_delete_event,
                      NULL);

    scrolled_win = gtk_scrolled_window_new (NULL, NULL);
    gtk_scrolled_window_set_shadow_type (GTK_SCROLLED_WINDOW (scrolled_win),
                                         GTK_SHADOW_IN);
    gtk_widget_show (scrolled_win);
    gtk_container_add (GTK_CONTAINER (window), scrolled_win);

    canvas = goo_canvas_new ();
    gtk_widget_set_size_request (canvas, 900, 700);
    goo_canvas_set_bounds (GOO_CANVAS (canvas), 0, 0, 1000, 1000);
    gtk_widget_show (canvas);
    gtk_container_add (GTK_CONTAINER (scrolled_win), canvas);

    root = goo_canvas_get_root_item (GOO_CANVAS (canvas));

    int i;
    const gdouble radius = 300;
    const gdouble bead_radius = 10;
    const gdouble stem_spacing = radius * M_PI * 2 / 56;
    const gdouble x_offset = radius + (stem_spacing * 4) + 50;
    const gdouble y_offset = 325;
    for (i = 0; i < 4; i++) {
        gdouble x = (x_offset - radius - stem_spacing * 4) + (stem_spacing * i);
        gdouble y = y_offset;
        g_beads[i] = goo_canvas_ellipse_new(root, x, y, bead_radius, bead_radius,
                                          "fill-color", "#000000", NULL);
    }

    for (i = 4; i < 60; i++) {
        double angle = (M_PI * 2 / 56 * (i - 4)) - M_PI;
        gdouble x = x_offset + radius * cos(angle);
        gdouble y = y_offset + radius * sin(angle);
        //printf("(%f, %f)\n", x, y);
        g_beads[i] = goo_canvas_ellipse_new(root, x, y, bead_radius, bead_radius,
                                          "fill-color", "#000000", NULL);
    }

    //gtk_idle_add_priority(G_PRIORITY_LOW, gtksim_update_beads, this);
    //gtk_idle_add_priority(500, gtksim_update_beads, this);

    m_gtk_ready = true;
                                        
    /* Pass control to the GTK+ main event loop. */
    gtk_main ();

    return;
}
