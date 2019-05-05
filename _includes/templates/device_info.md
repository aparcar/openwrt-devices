{% assign device = site.data.devices[page.device] %}

{% if device.vendor contains 'TP-Link' %}
{% include templates/install_tplink.md %}
{% endif %}

{% if device.recovery_method_s contains 'TFTP' %}
{% include templates/recovery_tftp.md %}
{% endif %}

{%- if device.switch_ports %}
### Switch Ports (for VLANs)

| Switch port | Port |
|:---         | ---: |
{%- for port in device.switch_ports %}
| {{ port[0] }} | {{ port[1] }} |
{%- endfor %}
{%- endif %}

{% if device.comments or device.wlan_comments %}

### Comments

{% if device.comments %}

#### General

{{ device.comments }}
{% endif %}

{% if device.wlan_comments %}

#### WLAN

{{ device.wlan_comments }}
{% endif %}

{% if device.comment_recovery %}

#### Recovery

{{ device.comment_recovery }}
{% endif %}

{% if device.comment_installation %}

#### Installation

{{ device.comment_installation }}
{% endif %}

{% endif %}

{% if device.flash_layout %}

### Flash layout

<pre>{{ device.flash_layout }}</pre>
{% endif %}
