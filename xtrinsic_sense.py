import time

class MMA8491:
  # Register values
  REG_STATUS = 0x00
  REG_X_MSB = 0x01
  REG_X_LSB = 0x02
  REG_Y_MSB = 0x03
  REG_Y_LSB = 0x04
  REG_Z_MSB = 0x05
  REG_Z_LSB = 0x06
  
  def __init__(self, bus, gpio, address = 0x55, en_pin = 22):
    self.bus = bus
    self.address = address
    self.en_pin = en_pin
    self.gpio = gpio
    self.gpio.setwarnings(False)
    self.gpio.setup(self.en_pin, self.gpio.OUT)
    self.gpio.setwarnings(True)
    self.gpio.output(self.en_pin, False)
    self.gpio.output(self.en_pin, True)

  def status(self):
    status = bus.read_byte_data(self.address, self.REG_STATUS)
    return status
    

  def axes(self):
    axes = [];
  
    # Set the sensor in ACTIVE mode
    self.gpio.output(self.en_pin, False)
    self.gpio.output(self.en_pin, True)
    time.sleep(0.001)
    
  
    data = self.bus.read_i2c_block_data(self.address, self.REG_X_MSB, 6)
    # X axis
    axes.append((data[0] << 6) + (data[1] & 0x3F))
    # Y axis
    axes.append((data[2] << 6) + (data[3] & 0x3F))
    # Z axis
    axes.append((data[4] << 6) + (data[5] & 0x3F))
    
    # Set the sensor in STANDBY mode
    return axes

class MAG3110:

  def __init__(self, bus, gpio, address = 0x55, en_pin = 22):
    self.bus = bus
    self.address = address
    self.en_pin = en_pin
    self.gpio = gpio
    self.gpio.setwarnings(False)
    self.gpio.setup(self.en_pin, self.gpio.OUT)
    self.gpio.setwarnings(True)
    self.gpio.output(self.en_pin, False)
    self.gpio.output(self.en_pin, True)
