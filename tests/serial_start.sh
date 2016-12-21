echo -n 0 > /sys/bus/platform/devices/sunxi_usb_udc/otg_role
modprobe g_serial
echo -n 2 > /sys/bus/platform/devices/sunxi_usb_udc/otg_role
