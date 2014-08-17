import time

class MMA8491:
  "Class to interface with Xtrinsic MMA8491 acceleration sensor"
   
  "Register values"
  REG_STATUS = 0x00
  REG_X_MSB = 0x01
  REG_X_LSB = 0x02
  REG_Y_MSB = 0x03
  REG_Y_LSB = 0x04
  REG_Z_MSB = 0x05
  REG_Z_LSB = 0x06
  
  def __init__(self, bus, gpio, address = 0x55, en_pin = 22):
    "Initialise the MMA8491 acceleration sensor"
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
    """Read the status register:
    bit 0: X data ready
    bit 1: Y data ready
    bit 2: Z data ready
    bit 3: data ready for all channels"""
    status = bus.read_byte_data(self.address, self.REG_STATUS)
    return status
    

  def axes(self):
    "Fetch data for all axes"
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
    
    return axes

class MAG3110:
  "Class to interface with Xtrinsic MAG3110 magnetic field sensor"

  REG_STATUS = 0x00
  REG_X_MSB = 0x01
  REG_X_LSB = 0x02
  REG_Y_MSB = 0x03
  REG_Y_LSB = 0x04
  REG_Z_MSB = 0x05
  REG_Z_LSB = 0x06
  REG_CTRL1 = 0x10

  " Bit fields for REG_CTRL1 "
  CTRL1_DR0 = 5 # Output data rate selection, default: 000.
  CTRL1_OS0 = 3 # Configure the over sampling ratio for the measurement, default: 00
  CTRL1_FR  = 2 # Fast Read selection, default: 0
  CTRL1_TM  = 1 # Trigger immediate measurement, default: 0
  CTRL1_AC  = 0 # Operating mode selection, default: 0 (standby).

  " Oversampling rates "
  OS_16  = 0 # Oversample ratio of 16
  OS_32  = 1 # Oversample ratio of 32
  OS_64  = 2 # Oversample ratio of 64
  OS_128 = 3 # Oversample ratio of 128

  def __init__(self, bus, address = 0x0E):
    """Initialise the sensor for default operating mode
    Default data rate and over sampling ratio are
    80.00 Hz and 16 sample average. """

    self.bus = bus
    self.address = address

    "Configure the sensor for default operating mode"
    control_byte = 1 << self.CTRL1_AC
    self.config(control_byte)

  def axes(self):
    "Fetch data for all axes"
    axes = [];

    data = self.bus.read_i2c_block_data(self.address, self.REG_X_MSB, 6)
    # X axis
    axes.append((data[0] << 8) + data[1])
    # Y axis
    axes.append((data[2] << 8) + data[3])
    # Z axis
    axes.append((data[4] << 8) + data[5])

    return axes

  def config(self, data):
    "Configure the sensor for a specific mode"
    self.bus.write_byte_data(self.address, self.REG_CTRL1, data)

class MPL3115:
  "Class to interface with Xtrinsic MPL3115 Precision Altimeter"

  REG_STATUS = 0x00
  REG_P_MSB = 0x01
  REG_P_CSB = 0x02
  REG_P_MSB = 0x03
  REG_T_MSB = 0x04
  REG_T_LSB = 0x05
  REG_CTRL1 = 0x26

  " Bit fields for REG_CTRL1 "
  CTRL1_MODE = 7 # Configure whether the sensor works as barometer(0) or altimeter (1), default: 0
  CTRL1_OS0  = 3 # Configure the over sampling ratio for the measurement, default: 00
  CTRL1_FR   = 2 # Fast Read selection, default: 0
  CTRL1_AC   = 0 # Operating mode selection, default: 0 (standby).

  " Oversampling rates "
  OS_1   = 0 # Oversample ratio of 1
  OS_2   = 1 # Oversample ratio of 2
  OS_4   = 2 # Oversample ratio of 4
  OS_8   = 3 # Oversample ratio of 8
  OS_16  = 4 # Oversample ratio of 16
  OS_32  = 5 # Oversample ratio of 32
  OS_64  = 6 # Oversample ratio of 64
  OS_128 = 7 # Oversample ratio of 128

  def __init__(self, bus, address = 0x60):
    """Initialise the sensor for default operating mode
    Default data rate and over sampling ratio are
    80.00 Hz and 16 sample average. """

    self.bus = bus
    self.address = address
    self.barometer = True

    """
    Configure the sensor for default operating mode
    The default operating mode is an oversampling rate of 8
    """
    control_byte  =         1 << self.CTRL1_AC
    control_byte |= self.OS_8 << self.CTRL1_OS0
    self.config(control_byte)

  def pressure(self):
    "Fetch pressure data"
    data = []

    data = self.bus.read_i2c_block_data(self.address, self.REG_P_MSB, 3)

    if self.barometer:
      "Barometer values are in Q16.4 format"
      retval  = data[0] << 24
      retval |= data[1] << 16
      retval |= data[2] <<  8
      retval /= 65536.0
    else:
      "Altimeter values are in Q18.2 format"
      retval  = data[0] << 24
      retval |= data[1] << 16
      retval |= data[2] <<  8
      retval /= 64.0

    return retval

  def temperature(self):
    "Fetch termperature data"
    data = []

    data = self.bus.read_i2c_block_data(self.address, self.REG_T_MSB, 2)
    print data

    "temperature values are in Q12.4 format"
    retval  = data[0] << 8
    retval |= data[1] << 0
    retval /= 256.0

    return retval

  def config(self, data):
    "Configure the sensor for a specific mode"
    print "address: 0x%02X, ctrl1: 0x%02X" % (self.address, self.REG_CTRL1)
    self.bus.write_byte_data(self.address, self.REG_CTRL1, data)
