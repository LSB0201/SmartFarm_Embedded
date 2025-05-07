import spidev

class MCP3008:
    def __init__(self, spi_channel=0):
        self.spi = spidev.SpiDev()
        self.spi.open(0, spi_channel)
        self.spi.max_speed_hz = 1350000
    
    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        return ((adc[1] & 3) << 8) + adc[2]
    
    def close(self):
        self.spi.close()  # SPI 연결 해제
