#!/usr/bin/python

from time import sleep

class PianoBar(object):
  pianobar_cmd = "/var/lib/pianobar/stdin.fifo"
  pianobar_log = "/var/lib/pianobar/pianobar.log"
  last_channel = 0
  command_map = {
    "love": "+",
    "ban": "-",
    "pause": "p",
    "next": "n"
  }

  def __init__(self):
    for k,v in self.command_map.iteritems():
      def foo(self):
        open(self.pianobar_cmd, "w").write(v+"\n")
      from types import MethodType
      self.__dict__[k] = MethodType(foo, PianoBar)

  def start(self, username, password, channel):
    from subprocess import call
    call(["/sbin/service", "pianobar", "start"])
    open(self.pianobar_cmd, "w").write(username+"\n"+password+"\n")
    sleep(2)
    self.change(channel)

  def stop(self):
    from subprocess import call
    call(["/sbin/service", "pianobar", "stop"])

  def change(self, channel):
    open(self.pianobar_cmd, "w").write("s\n"+str(channel)+"\n")
    self.last_channel = channel

  def channels(self):
    import re
    log = open(self.pianobar_log, "r")
    log.seek(0,2) # seek to the end of the file
    open(self.pianobar_cmd, "w").write("s\n"+str(self.last_channel)+"\n")
    ret = []
    matcher = re.compile(".*\D(\d+)\)\s\s*[a-zA-Z]\s\s*(\S.*)$")
    sleep(1)
    for line in log.readlines():
      result = matcher.match(line)
      if result:
        ret.append((int(result.group(1)), result.group(2)))
    return ret

  def info(self):
    import re
    log = open(self.pianobar_log, "r")
    log.seek(0,2) # seek to the end of the file
    open(self.pianobar_cmd, "w").write("i\n")
    ret = ""
    matcher = re.compile(".*[^\"]\"([^\"]+)\"[^\"]*\"([^\"]+)\"[^\"]*\"([^\"]+)\"")
    sleep(1)
    ret = []
    for line in log.readlines():
      result = matcher.match(line)
      if result:
        ret.append({"title":result.group(1), "artist":result.group(2), "album":result.group(3)})
    return ret[-1]
    
if __name__ == "__main__":
  pass
