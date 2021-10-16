"""
    This file is part of https://github.com/dovydenkovas/autocar project.

    Copyright 2021 The https://github.com/dovydenkovas/autocar contributors


    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import os, subprocess, time, serial


# this script lets you emulate a serial device
# the client program should use the serial port file specifed by client_port

# if the port is a location that the user can't access (ex: /dev/ttyUSB0 often),
# sudo is required

class ArduinoEmulator(object):
    def __init__(self, device_port='./.arduinoTTY', client_port='/dev/ttyUSB0'):
        self.device_port = device_port
        self.client_port = client_port

        cmd=[ '/usr/bin/socat','-d','-d',
              'PTY,link=%s,raw,echo=0' % self.device_port,
              'PTY,link=%s,raw,echo=0' % self.client_port
            ]

        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        time.sleep(1)
        self.serial = serial.Serial(self.device_port, 9600, rtscts=True, dsrdtr=True)
        self.err = ''
        self.out = ''

    def write(self, out):
        self.serial.write(out)

    def read(self):
        line = b''
        while self.serial.inWaiting() > 0:
            line += self.serial.read(1)
        return line

    def __del__(self):
        self.stop()

    def stop(self):
        self.proc.kill()
        self.out, self.err = self.proc.communicate()

    def mainloop(self):
        while True:
            self.read()

arduino = ArduinoEmulator()
arduino.mainloop()
