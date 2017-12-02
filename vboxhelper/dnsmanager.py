import dns.zone
import dns.name
import dns.rdtypes.ANY.SOA
import dns.rdtypes.ANY.NS
import dns.rdtypes.IN.A

class dnsmanager():
    """DNS manager class. Interfaces with dnspython"""

    def __init__(self, bind_configpath):
        """
        dnsmanager Constructor

        Args:
            bind_configpath: Bind path to zones and config
        """
        self.bind_configpath = bind_configpath

    def update(self, hostname, externalip, internalip, hostlist):
        origin = dns.name.from_text(hostname + ".")
        admin = dns.name.from_text("admin.host.com.")
        nstarget = dns.name.from_text("ns.host.com.")
        rdataclassin = dns.rdataclass.from_text("IN")
        rdatatypesoa = dns.rdatatype.from_text("SOA")
        rdatatypens = dns.rdatatype.from_text("NS")
        rdatatypea = dns.rdatatype.from_text("A")

        zone = dns.zone.Zone( origin, rdataclassin)

        nodeorigin = zone.find_node(origin, True)
        nodeint = zone.find_node(dns.name.from_text("int", origin), True)

        soardataset = nodeorigin.find_rdataset(rdataclassin, rdatatypesoa, 0, True)
        aoriginrdataset = nodeorigin.find_rdataset(rdataclassin, rdatatypea, 0, True)
        nsrdataset = nodeorigin.find_rdataset(rdataclassin, rdatatypens, 0, True)
        aintrdataset = nodeint.find_rdataset(rdataclassin, rdatatypea, 0, True)

        soarecord = dns.rdtypes.ANY.SOA.SOA(rdataclassin, rdatatypesoa, origin, admin, 1, 3600, 3600, 24600, 24600)
        nsrecord = dns.rdtypes.ANY.NS.NS(rdataclassin, rdatatypens, nstarget)
        aoriginrecord = dns.rdtypes.IN.A.A(rdataclassin, rdatatypea, externalip)
        aintrecord = dns.rdtypes.IN.A.A(rdataclassin, rdatatypea, internalip)

        soardataset.add(soarecord)
        aoriginrdataset.add(aoriginrecord)
        nsrdataset.add(nsrecord)
        aintrdataset.add(aintrecord)

        print(zone.to_text().decode("utf-8"))

        conf = ""
        hostlist.append(hostname)
        for host in hostlist:
            conf += """zone "{0}." {{
                       type master;
                    file "{0}.zone";
                    }};
                    """.format(host)
        print(conf)


#Debug
d = dnsmanager("foo")
d.update("foo", "192.168.56.1", "192.168.100.1", [])
