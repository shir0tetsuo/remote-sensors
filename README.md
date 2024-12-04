# Purpose
Implement the ds3231 RTC module & Waveshare 3.14 inch V4 onto Raspberry Pi Zero 2 W Installation, BME280, lights

![image](https://github.com/user-attachments/assets/3f4a6f6d-7d98-48c1-b089-7ba0cafc9a20)
![image](https://github.com/user-attachments/assets/68c51b69-dba1-4731-8db1-644b9f3976d9)
![image](https://github.com/user-attachments/assets/3cb9ddbe-a53b-4549-ab7a-ac1bbf08e7f0)
![image](https://github.com/user-attachments/assets/ccd5462b-bf9f-4625-9d89-dd836bc1efc8)

This is a project that involves soldering if you want to and I added a weather-proof case around the build but it's not necessarily necessary nor is the WaveShare display. I will not be going over which pins are used, but you may have to get creative 😉️

# Preparation
(Flash media using Raspberry Pi's flashing software to Micro SD)

- Follow steps to connect to your wifi network.
- Set hostname as "sensors"
- Ensure a default WiFi is provided.

ssh -> pi@sensors.local

```bash
#!/bin/bash
# Follow steps to enable interfaces i2c, spi
raspi-config

sudo apt update
sudo apt install -y python3-smbus python3-bme280 # if not already
sudo apt install -y i2c-tools

sudo modprobe i2c-dev
echo "i2c-dev" | sudo tee -a /etc/modules

# Bind 0x77 (Modify to your setup) RTC to module
sudo bash -c 'echo ds3231 0x77 > /sys/class/i2c-adapter/i2c-1/new_device'
sudo hwclock -s

# put in /boot/config.txt on the boot disk (at end)
# and add the following if missing:
#dtparam=i2c_arm=on
#dtparam=i2c1=on
# -- and of course --
# "dtoverlay=i2c-rtc,ds3231"

# restart if needed.

# If the RTC is UU, it has been detected:
sudo i2cdetect -y 1
```
My setup yields this result at modprobe:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- UU -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- 77
```

```bash
# Set RTC clock to HW clock
sudo hwclock -r
sudo hwclock -w

# disable fake clock
sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo systemctl disable fake-hwclock

# start original hwclock script:
# COMMENT OUT:
#if [ -e /run/systemd/system ] ; then
# exit 0
#fi
sudo nano /lib/udev/hwclock-set
```

The rest of the programs in this repository are used for maintaining an internet connection and relaying the sensor information.

Todo: Implement documentation on Waveshare display (when I figure it out)

