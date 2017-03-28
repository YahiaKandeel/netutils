#!/usr/bin/python
from netutils import netconf

# Cred.
username = 'XXX'
password = 'XXX'
host = 'XXX'

# XML Command
command = '''
<rpc message-id="12">
<get-config>
    <source>
        <running/>
    </source>
</get-config>
</rpc>'''

# Connect
nf = netconf.NetConf(host, username, password)
if nf.connect():
    # if connected, Execute command
    result = nf.execute(command)
    # Exit
    nf.close()
    # Print result
    print result
