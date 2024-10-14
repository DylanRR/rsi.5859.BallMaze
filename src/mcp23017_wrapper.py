
import digitalio
from time import sleep
from adafruit_mcp230xx.mcp23017 import MCP23017

class MCP_LED:
  def __init__(self, mcpObj: MCP23017, channel):
    self._mcp = mcpObj
    self._mcp_pin = self._mcp.get_pin(channel)
    self._mcp_pin.direction = digitalio.Direction.OUTPUT
    self._mcp_pin.value = False

  def close(self):
    self._mcp_pin = None
    self._mcp = None

  def turnOn(self):
      self._mcp_pin.value = True
  
  def turnOff(self):
      self._mcp_pin.value = False
    
  def getState(self):
    return self._mcp_pin.value

  def ledBlink(self, duration=1):
    self.turnOn()
    sleep(duration)
    self.turnOff()
    sleep(duration)


class MCP_BTN:
    def __init__(self, mcpObj: MCP23017, channel, debounce_time=0.005):
        self._mcp_pin = mcpObj.get_pin(channel)
        self._mcp_pin.direction = digitalio.Direction.INPUT
        self._mcp_pin.pull = digitalio.Pull.UP  # Enable pull-up resistor for input channels
        self._debounce_time = debounce_time
        self._pressed = False

    def _debounce(self):
        state = self._mcp_pin.value
        consistent_readings = 0
        for _ in range(5):  # Check the state 5 times
            sleep(self._debounce_time)
            if self._mcp_pin.value == state:
                consistent_readings += 1
            else:
                consistent_readings = 0
                state = self._mcp_pin.value
            if consistent_readings >= 5:
                return state
        return state

    def is_pressed(self):
        if self._debounce() == False:  # Assuming active low buttons
            self._pressed = True
        return self._pressed

    def reset(self):
        self._pressed = False

