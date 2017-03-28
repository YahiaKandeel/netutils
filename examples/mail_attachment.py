#!/usr/bin/python
from netutils import mailer

# Configure
server = 'x.x.x.x'
Att = 'path/to/your/attachment'
From = 'LDAP Report<reporter@local.me>'
To = 'Yahia Kandeel<yahia@local.me>'
Subject = 'Report'
Body = '<br /><br /><br /><p>Best Regards,</p>'

# Zip Attachment
attachment_name, data = mailer.zip(Att)
Attachment_Type = 'zip'

# Create Message
msg = mailer.message(
    From,  # From
    To,  # To
    Subject,  # Subject
    Body,  # Body
    Attachment_Data=data,
    Attachment_Filename=attachment_name,
    Attachment_Type=Attachment_Type
)


# Send The Message
mailer.send(server, From, To, msg)
