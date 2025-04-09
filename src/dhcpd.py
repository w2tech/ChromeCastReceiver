"""
Startet einen DHCP-Server mit udhcpd
Erstellt eine temporäre Konfigurationsdatei
Vergibt eine feste IP-Adresse an den Client
"""

class Dhcpd():
    """DHCP server daemon running in background."""

    def __init__(self, interface):
        """Constructor accept an interface to listen."""
        self.dhcpd = None
        self.interface = interface

    def start(self):
        fd, self.conf_path = tempfile.mkstemp(suffix='.conf')
        conf = "start  {}\nend {}\ninterface {}\noption subnet {}\noption lease {}\n".format(
            Settings.peeraddress, Settings.peeraddress, self.interface, Settings.netmask, Settings.timeout)
        with open(self.conf_path, 'w') as c:
            c.write(conf)
        self.dhcpd = subprocess.Popen(["sudo", "udhcpd", self.conf_path])

    def stop(self):
        if self.dhcpd is not None:
            self.dhcpd.terminate()
            self.conf_path.unlink()
