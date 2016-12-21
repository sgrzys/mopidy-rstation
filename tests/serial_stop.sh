echo -n 0 > /sys/bus/platform/devices/sunxi_usb_udc/otg_role
rmmod g_serial
echo -n 1 > /sys/bus/platform/devices/sunxi_usb_udc/otg_role
