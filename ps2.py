# micropython ESP32
# PS/2 keyboard and mouse emulator

# AUTHOR=EMARD
# LICENSE=BSD

from time import sleep_us
from machine import Pin
from micropython import const
from uctypes import addressof

class ps2:
  def __init__(self):
    self.led = Pin(5, Pin.OUT)
    self.led.off()
    self.init_pinout() # communicate using SD card pins when SD is inactive
    self.init_pins()
    self.qdelay = const(14) # quarter-bit delay

  @micropython.viper
  def init_pinout(self):
    self.gpio_kbd_clk  = const(14) # sd_clk
    self.gpio_kbd_data = const(15) # sd_cmd

  def init_pins(self):
    self.kbd_clk  = Pin(self.gpio_kbd_clk,  Pin.OUT)
    self.kbd_data = Pin(self.gpio_kbd_data, Pin.OUT)

  @micropython.viper
  def write(self, data):
    p = ptr8(addressof(data))
    l = int(len(data))
    for i in range(l):
      val = p[i]
      parity = 1
      self.kbd_data.off()
      sleep_us(self.qdelay)
      self.kbd_clk.off()
      sleep_us(self.qdelay+self.qdelay)
      self.kbd_clk.on()
      sleep_us(self.qdelay)
      for nf in range(8):
        if val & 1:
          self.kbd_data.on()
          parity ^= 1
        else:
          self.kbd_data.off()
          parity ^= 0 # keep timing the same as above
        sleep_us(self.qdelay)
        self.kbd_clk.off()
        val >>= 1
        sleep_us(self.qdelay+self.qdelay)
        self.kbd_clk.on()
        sleep_us(self.qdelay)
      if parity:
        self.kbd_data.on()
      else:
        self.kbd_data.off()
      sleep_us(self.qdelay)
      self.kbd_clk.off()
      sleep_us(self.qdelay+self.qdelay)
      self.kbd_clk.on()
      sleep_us(self.qdelay)
      self.kbd_data.on()
      sleep_us(self.qdelay)
      self.kbd_clk.off()
      sleep_us(self.qdelay+self.qdelay)
      self.kbd_clk.on()
      sleep_us(self.qdelay)