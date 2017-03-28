##################################################################
###### Netconf Module ..
###### Wrapped over paramiko ..
###### By: Yahia Kandil<yahia.kandil@gmail.com>
##################################################################
import paramiko
import socket

class NetConf():
	def __init__(self, host, user, passwd):
		self.user 	= user
		self.host 	= host
		self.passwd = passwd
		self.socket = None
		self.trans 	= None
		self.netconf_session = None
		self.result = {}

	def connect(self):
		#Initialize the ssh paramiko client
		ssh = paramiko.SSHClient()
		#load keys from known_hosts file
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		#create TCP socket
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			# Bind TCP socket to port 22 on given host
			self.socket.connect((self.host, 22))
			# Get the transport layer from SSH Client
			self.trans = paramiko.Transport(self.socket)
			# Connect to remote host using provided credentials
			self.trans.connect(username=self.user, password=self.passwd)
			# Open a session
			self.netconf_session = self.trans.open_session()
			# rename the session
			name = self.netconf_session.set_name('netconf')
			# use netconf protocol
			self.netconf_session.invoke_subsystem('netconf')
			return True
		except:
			print "Coudln't connect to host", self.host
			return False

	def execute(self, command, starting_clause='<rpc', ending_clause='</rpc'):
		# Initialize the result, read, done
		self.result[command], result, read, done = '', '', False, False
		# send the xml command
		self.netconf_session.send(command)
		# get first result iteration
		data = self.netconf_session.recv(1024)
		while data:
			result += data
			# check if we done
			if ending_clause in data :break
			# read data, and convert it to list
			data = self.netconf_session.recv(1024)
		### retrun
		self.result[command] = result
		return self.result[command]

	def close(self, command='<rpc><close-session/></rpc>'):
		try:
			#### Sending close Command
			self.netconf_session.send(command)
			#### Close Netconf_session
			self.netconf_session.close()
			#### Closing Transport Layer session
			self.trans.close()
			#### Closing Socket.
			self.socket.close()
			return True
		except:
			return False

##################################################################
###### Testing...
##################################################################
# vpn = netconf(host, user, passwd)
# vpn.connect()
# vpn.execute(command)
# vpn.close()