{% assign device = site.data.devices[page.device] %}
{% assign image_factory = device.firmware_openwrt_install_url | split: "/" | last %}
### Flashing via TFTP

Pressing the WPS/Reset button during powerup makes the bootstrap loader enter
the TFTP recovery mode. The procedure can be used to transfer a firmware image:

* assign **{{ device.tftp_ip }}** to your local network interface 
* publish a firmware image via tftp: `cp {{ image_factory }} /srv/tftp/{{ device.tftp_image }}`
* configure your tftp server
* wait for the firmware transfer (about 20s), firmware flash (about 90s) and subsequent reboot (about 30s)


