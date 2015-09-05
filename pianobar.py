#!/usr/bin/python

class PianoBar(object):
  pianobar_cmd = "/var/lib/pianobar/stdin.fifo"
  last_channel = 0
  command_map = {
    "love": "+",
    "ban": "-",
    "info": "i",
    "pause": "p",
    "next": "n",
    "change": "s"
  }

  def __init__(self):
    pass
