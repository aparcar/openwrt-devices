{% assign device = site.data.devices[page.device] %}
{% assign image_factory = device.firmware_openwrt_install_url | split: "/" | last %}
### Flashing via TFTP

* Download the factory firmware image offered above to your Computer.
* Configure a computer with static IP {{ device.tftp_ip }}/24 and a TFTP server.
  On Debian or Ubuntu you can use either the *tftpd-hpa* or *tftpd* server
  packages.
* Rename the downloaded firmware image to `{{ device.tftp_image }}` and place it
  in the tftp server's root directory. (If using **tftpd-hpa** this is
  `/var/lib/tftpboot/`; if **tftpd**, it is `/srv/tftp/`) You can test that the
  file is downloadable with `tftp localhost and get {{ device.tftp_image }}`.
* Connect the computer to one of the router's Ethernet ports while the router is
  off. Press and keep pressed the router's reset button and power it up. After
  about 7-10 seconds release the reset button. The power LED will flicker
  rapidly for ~3 seconds, indicating download of the firmware file.
* The router will write the firmware to flash during ~40 more seconds of
  occasional power LED blinks, and then will reboot by itself, ready for use.
