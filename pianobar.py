#!/usr/bin/python

from celery import Celery
from pexpect import spawn
from pexpect import EOF as PEXPECT_EOF

app = Celery('pianobar', broker='amqp://guest@localhost//')

pianobar_exe = "/root/pianobar/pianobar"
pianobar_pexpect = None

last_channel = 0

command_map = {
    "love": "+",
    "ban": "-",
    "info": "i",
    "pause": "p",
    "next": "n",
    "change": "s"
}

@app.task
def start(username, password, channel):
    if pianobar_pexpect:
        return -1
    pianobar_pexpect = spawn(pianobar_exe)
    pianobar_pexpect.expect('Welcome.*')
    pianobar_pexpect.expect_exact('[?] Email: ')
    pianobar_pexpect.sendline(username)
    pianobar_pexpect.expect_exact('[?] Password: ')
    pianobar_pexpect.sendline(password)
    index = pianobar_pexpect.expect_exact(['(i) Login... Ok.', '(i) Login... Error: Wrong email address or password.'])
    if index == 1:
        pianobar_pexpect.expect(PEXPECT_EOF)
        if pianobar_pexpect.isalive():
            pianobar_pexpect.wait()
        pianobar_pexpect = None
        return -2
    logfile = open("/tmp/pianobar.log", "wb")
    pianobar_pexpect.logfile = logfile
    pianobar_pexpect.sendline(last_channel)
    return 0


