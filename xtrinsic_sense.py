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
    print "address: 0x%02X, en_pin: %d" % (address, en_pin)
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
    axes.append((data[0] << 8) + data[1])
    # Y axis
    axes.append((data[2] << 8) + data[3])
    # Z axis
    axes.append((data[4] << 8) + data[5])
    
    # Set the sensor in STANDBY mode
    return axes
