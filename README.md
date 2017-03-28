# netutils
The aim of this module to provide the network utils that would be needed by any netword administrator

## prequests
** paramiko 
** zipfile
** argparse

## NetConf  
netconf module, wrapped over Paramiko 
```python
#!/usr/bin/python
from netutils import netconf

#### Cred.
username = 'XXX'
password = 'XXX'
host = 'XXX'

#### XML Command
command = '''
<rpc message-id="12">
<get-config>
	<source>
		<running/>
	</source>
</get-config>
</rpc>'''

##### Connect
nf = netconf.NetConf(host, username, password)
if nf.connect():
	#### if connected, Execute command
	result = nf.execute(command)
	#### Exit
	nf.close()
	#### Print result
	print result

```

## Mailer
Relay Emails through any SMTP relay ...
It supports the following:
* Attachments.
* Zip the Attachements.
* HTML Body

You should have SMTP Relay enabled.

mailer has a command line interface as well as you can use it as a module
to use the command line interface you should configure the SMTP Relay inside the script itself.
The supported options as follows:
```bash
yahia@yahia-lp ~/D/d/netutils> ./mailer.py --help
usage: mailer.py [-h] [--From FROM] [--body BODY]
                 [--bodyfilename BODYFILENAME] [--attachment ATTACHMENT]
                 [--zip] [--date]
                 subject to

positional arguments:
  subject               Subject
  to                    Recipients - Comma seprated for multi users between
                        double quotes

optional arguments:
  -h, --help            show this help message and exit
  --From FROM, -F FROM  From
  --body BODY, -b BODY  Message Body
  --bodyfilename BODYFILENAME
                        Read message body from a file
  --attachment ATTACHMENT, -a ATTACHMENT
                        Add Attachment
  --zip, -z             Zip Attachement
  --date, -d            Add Date To Header
```

To use it as a python module

```python
#!/usr/bin/python
from netutils import mailer

##### Configure
server  = 'x.x.x.x'	### SMTP Relay IP
Att 	= 'path/to/your/attachment'
From 	= 'LDAP Report<reporter@local.me>'
To   	= 'Yahia Kandeel<yahia@local.me>'
Subject = 'Report'
Body	= '<br /><br /><br /><p>Best Regards,</p>'

##### Zip Attachment
attachment_name, data = mailer.zip(Att)
Attachment_Type = 'zip'

#### Create Message
msg = mailer.message(
			From,  					### From
			To, 	 				### To
			Subject, 				### Subject
			Body, 					### Body
			Attachment_Data = data, 	
			Attachment_Filename = attachment_name, 
			Attachment_Type = Attachment_Type
		)


#### Send The Message
mailer.send(server, From, To, msg)
```