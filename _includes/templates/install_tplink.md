{% assign device = site.data.devices[page.device] %}
{% assign image_factory = device.firmware_openwrt_install_url | split: "/" | last %}

## Installation

### Flashing via webinterface

* Download the factory firmware image offered above to your Computer.
* Connect your Computer to a LAN port of the TP-link. If the configuration was
  not changed, the DHCP on the router will give you a 192.168.0.X address and
  the TP-link web administration page is [192.168.0.1](http://192.168.0.1/).
  (User: **admin**, Password: **admin**) Under *System Tools* select *Firmware
  Upgrade*. Browse to the previously downloaded **{{ image_factory }}** file.
  Click *Upgrade*.
* If the Webinterface tells you *You have no authority to access this router!*
  that's because your browser does not send the correct HTTP referer header.
  Disable addons or use a different browser.
* Connect to [192.168.1.1](http://192.168.1.1) with your web browser
* Set your password and configure the router through the web UI. Basic Config
  Congratulations! You just installed OpenWrt on your Router!

