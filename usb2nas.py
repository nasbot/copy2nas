from evdev import InputDevice, ecodes
import shutil, errno
import time
import os
import logging

logging.basicConfig(filename='/var/log/usb2nas.log',level=logging.DEBUG)
logging.info('--- v1.4 copy2nas started at %s ---', str(time.asctime()))
# Copy function from USB to Local Disk
def copyanything(src, dst):
	try:
        	shutil.copytree(src, dst)
	except OSError as exc: # python >2.5
        	if exc.errno == errno.ENOTDIR:
            		shutil.copy(src, dst)
			logging.info('Copied %s', dst)
        	else: raise


dev = InputDevice('/dev/input/event0')
srcUsb = '/media/usb0'
srcSdcard = '/media/sdcard'
dst = '/var/lib/owncloud/data/adimitrov/files/'
snd = '/usr/bin/aplay /var/lib/owncloud/im-so-ready.wav'

for event in dev.read_loop():
	if event.type == ecodes.EV_KEY:
		if event.code == 226 and event.value == 00:
			copyanything(srcUsb, dst + 'From_USB_' + str(time.asctime()))
			os.system(snd)
			logging.info('--- usb2nas finished at %s ---', str(time.asctime()))
		elif event.code == 113 and event.value == 00:
			os.system("mount /dev/mmcblk0p1")
			copyanything(srcSdcard, dst + 'From_SDCARD_' + str(time.asctime()))
                        os.system(snd)
			logging.info('--- sdcard2nas finished at %s ---', str(time.asctime()))
			os.system("umount /dev/mmcblk0p1")
