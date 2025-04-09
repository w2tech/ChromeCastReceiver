class WpaCli:
    """
    Wraps the wpa_cli command line interface.
    """

    def __init__(self):
        self.logger = getLogger("PiCast")
        pass

    def cmd(self, arg):
        command_str = "sudo wpa_cli"
        command_list = command_str.split(" ") + arg.split(" ")
        p = subprocess.Popen(command_list, stdout=subprocess.PIPE)
        stdout = p.communicate()[0]
        return stdout.decode('UTF-8').splitlines()

    def start_p2p_find(self):
        self.logger.debug("wpa_cli p2p_find type=progressive")
        status = self.cmd("p2p_find type=progressive")
        if 'OK' not in status:
            raise PiCastException("Fail to start p2p find.")

    def stop_p2p_find(self):
        self.logger.debug("wpa_cli p2p_stop_find")
        status = self.cmd("p2p_stop_find")
        if 'OK' not in status:
            raise PiCastException("Fail to stop p2p find.")

    def set_device_name(self, name):
        self.logger.debug("wpa_cli set device_name {}".format(name))
        status = self.cmd("set device_name {}".format(name))
        if 'OK' not in status:
            raise PiCastException("Fail to set device name {}".format(name))

    def set_device_type(self, type):
        self.logger.debug("wpa_cli set device_type {}".format(type))
        status = self.cmd("set device_type {}".format(type))
        if 'OK' not in status:
            raise PiCastException("Fail to set device type {}".format(type))

    def set_p2p_go_ht40(self):
        self.logger.debug("wpa_cli set p2p_go_ht40 1")
        status = self.cmd("set p2p_go_ht40 1")
        if 'OK' not in status:
            raise PiCastException("Fail to set p2p_go_ht40")

    def wfd_subelem_set(self, val):
        self.logger.debug("wpa_cli wfd_subelem_set {}".format(val))
        status = self.cmd("wfd_subelem_set {}".format(val))
        if 'OK' not in status:
            raise PiCastException("Fail to wfd_subelem_set.")

    def p2p_group_add(self, name):
        self.logger.debug("wpa_cli p2p_group_add {}".format(name))
        self.cmd("p2p_group_add {}".format(name))

    def set_wps_pin(self, interface, pin, timeout):
        self.logger.debug("wpa_cli -i {} wps_pin any {} {}".format(interface, pin, timeout))
        status = self.cmd("-i {} wps_pin any {} {}".format(interface, pin, timeout))
        return status

    def get_interfaces(self):
        selected = None
        interfaces = []
        status = self.cmd("interface")
        for ln in status:
            if ln.startswith("Selected interface"):
                selected = re.match(r"Selected interface\s\'(.+)\'$", ln).group(1)
            elif ln.startswith("Available interfaces:"):
                pass
            else:
                interfaces.append(str(ln))
        return selected, interfaces

    def get_p2p_interface(self):
        sel, interfaces = self.get_interfaces()
        for it in interfaces:
            if it.startswith("p2p-wl"):
                return it
        return None

    def check_p2p_interface(self):
        if self.get_p2p_interface() is not None:
            return True
        return False
