import dns.zone
import dns.name
import dns.rdtypes.ANY.SOA
import dns.rdtypes.ANY.NS
import dns.rdtypes.IN.A

class VirZone:
    """
    Manage DNS Records
    """
    def from_file(filepath, originDomain = None):
        try:
            zoneData = open(filepath).read()
        except FileNotFoundError:
            print("File path incorrect")
            raise FileNotFoundError
        origin = dns.name.from_text(originDomain)
        zone = dns.zone.from_file(zoneData, self.origin)
        return VirZone(orignDomain, zone)

    def __init__(self, originDomain, zone = None):
        self.origin = dns.name.from_text(originDomain)
        if zone:
            self.zone = zone
        else:
            self.zone = dns.zone.Zone(self.origin)
            node = self.zone.find_node(self.origin, True)

    def AddSOARecord(self, admin = "admin.host.com.", serial=1, refresh=3600, retry=3600, expire=7200, minimum=26400):
        if type(admin) == str:
            admin = dns.name.from_text(admin)

        rdataset = self.zone[self.origin].find_rdataset(dns.rdataclass.from_text("IN"), dns.rdatatype.from_text("SOA"), 0, True)
        record = dns.rdtypes.ANY.SOA.SOA(dns.rdataclass.from_text("IN"), dns.rdatatype.from_text("SOA"),
                self.origin, admin, serial, refresh, retry, expire, minimum)
        rdataset.add(record)

    def AddNSRecord(self, value, name = None):
        if not name: name = self.origin
        else:
            if type(name) == str: name = dns.name.from_text(name)
            node = self.zone.find_node(name, True)

        rdataset = self.zone[name].find_rdataset(dns.rdataclass.from_text("IN"), dns.rdatatype.from_text("NS"), 0, True)
        record = dns.rdtypes.ANY.NS.NS(dns.rdataclass.from_text("IN"), dns.rdatatype.from_text("NS"), dns.name.from_text(value))
        rdataset.add(record)

    def AddARecord(self, value, name = None):
        if not name: name = self.origin
        else:
            if type(name) == str: name = dns.name.from_text(name)
            node = self.zone.find_node(name, True)

        rdataset = self.zone[name].find_rdataset(dns.rdataclass.from_text("IN"), dns.rdatatype.from_text("A"), 0, True)
        record = dns.rdtypes.IN.A.A(dns.rdataclass.from_text("IN"), dns.rdatatype.from_text("A"), value)
        rdataset.add(record)

    def GetZone(self):
        return self.zone.to_text().decode("utf-8")









