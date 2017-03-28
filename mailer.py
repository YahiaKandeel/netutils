#!/usr/bin/python
#################################################################
##### Mailer
##### Sends Emails that support attachements - Text & Zipped.
##### By: Yahia Kandil<yahia.kandil@gmail.com>
#################################################################
import smtplib
import datetime
import zipfile
import argparse
import sys
import os
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#################################################################
##### Configurations
#################################################################

##### Static Configuration
Server = "XXXXXXX"
today  = str(datetime.date.today())
From   = "Ldap Report<ldapReport@local.me>"

#################################################################
##### Support Function ... 
#################################################################

##### create & read Zip File
def zip(attachment):
	try:
		### Compressed File:
		compressed_file = os.path.basename(attachment).split('.')[0] + '.zip'
		### create compressed file
		output = zipfile.ZipFile(compressed_file, 'w')
		### Add attachment to it
		output.write(attachment, compress_type=zipfile.ZIP_DEFLATED)
		### Close compressed file
		output.close()
		## read Zip file
		data = open(compressed_file).read()
		## return data
		return compressed_file, data

	except:
		print "Can't create compressed file"
		return False


##### Construct Message
def message(From, To, Subject, Body, Attachment_Data = False, Attachment_Filename = False , Attachment_Type = 'text'):

	##### Construct Message
	msg = MIMEMultipart()
	msg["From"]    = From
	msg["To"]      = To
	msg["Subject"] = Subject
	
	### Prepare Attachement ..
	if Attachment_Filename and Attachment_Data:
		### Set Type
		attachment = MIMEBase('application', Attachment_Type)
		### Add Payload
		attachment.set_payload(Attachment_Data)
		### Encode it
		encoders.encode_base64(attachment)
		### Add Header 
		attachment.add_header("Content-Disposition", "attachment", filename = Attachment_Filename)
		### Attach it to the message
		msg.attach(attachment)

	##### Attach Body
	body = MIMEText(Body, 'html')
	msg.attach(body)
	
	return msg

def send(Server, From, To, Message):
	try:
		##### Send Message
		server = smtplib.SMTP(Server)
		##### Helo
		server.ehlo()
		##### Send
		server.sendmail(From, To.split(','), Message.as_string())
		##### Close
		server.quit()

	except:
		print "Error in Seding Message!"

#################################################################
##### Command Line Args
#################################################################
def main():
	parser = argparse.ArgumentParser()

	### Mandatory 
	parser.add_argument('subject', help='Subject')
	parser.add_argument('to',      help='Recipients - Comma seprated for multi users between double quotes')

	### Optional
	parser.add_argument('--From',    	'-F' , help='From')
	parser.add_argument('--body', 		'-b' , help='Message Body')
	parser.add_argument('--bodyfilename'     , help='Read message body from a file')
	parser.add_argument('--attachment', '-a' , help='Add Attachment')
	parser.add_argument('--zip', 		'-z' , action='store_true', default = False ,help='Zip Attachement')
	parser.add_argument('--date', 		'-d' , action='store_true', default = False ,help='Add Date To Header')

	args = parser.parse_args()


	#################################################################
	##### Main Function ... 
	#################################################################
	if args.subject and args.to:
		
		#### To
		To = args.to
		#### Subject
		Subject = args.subject
		#### From
		if args.From:From = args.From
		#### Date
		if args.date:Subject += ' - ' + today
		
		#### Body
		if args.body: 
			Body = args.body
		elif args.bodyfilename:
			Body = open(args.bodyfilename).read()
		else:
			Body = '<p>Best Regards,</p>'

		#### if attachment  
		if args.attachment:

			attachment = args.attachment

			#### check if the zip flag enabled.
			if args.zip:
				attachment, data = zip(attachment)
				data_type = 'zip'

			else:
				data = open(attachment).read()
				data_type = 'text'

			msg = message(From, To, Subject, Body, Attachment_Data = data, 
							Attachment_Filename = attachment , Attachment_Type = data_type)

		#### If No Attachment !
		else:
			msg = message(From, To, Subject, Body)

		#### Send Message !
		send(Server, From, To, msg)

if __name__ == "__main__":
	main()