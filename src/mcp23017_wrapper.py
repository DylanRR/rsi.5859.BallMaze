import digitalio
from time import sleep
from adafruit_mcp230xx.mcp23017 import MCP23017

class MCP_CHANNEL:
  def __init__(self, mcpObj: MCP23017, channel, outputChannel=True):
    self._mcp = mcpObj
    self._mcp_pin = self._mcp.get_pin(channel)
    self._outputChannel = outputChannel
    if self._outputChannel:
      self._mcp_pin.direction = digitalio.Direction.OUTPUT
      self._mcp_pin.value = False
    else:
      self._mcp_pin.direction = digitalio.Direction.INPUT

  def close(self):
    if self._outputChannel:
      self._mcp_pin.value = False
    self._mcp_pin = None
    self._mcp = None

  def turnOn(self):
    if self._outputChannel:
      self._mcp_pin.value = True
    else:
      raise Exception("Cannot set an input channel")
  
  def turnOff(self):
    if self._outputChannel:
      self._mcp_pin.value = False
    else:
      raise Exception("Cannot set an input channel")
    
  def getState(self):
    self._mcp_pin.value

  def ledBlink(self, duration=1):
    if not self._outputChannel:
      raise Exception("Cannot blink an input channel")
    self.turnOn()
    sleep(duration)
    self.turnOff()
    sleep(duration)

