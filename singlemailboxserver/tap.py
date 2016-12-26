import service
import getpass
from twisted.python import usage,util
from twisted.application import internet

class Options(usage.Options):

    optParameters = [
        ["pop3port", None, 1100, "Port Number the POP3 server should listen on",int],
        ["pop3listen", None, '0.0.0.0',"IP address the POP3 server should listen on"],
        ["pop3username",None, getpass.getuser(),"POP3 username"],
        ["smtpport", None, 2500, "Port number the SMTP server should listen on",int],
        ["smtplisten", None, '127.0.0.1', "IP address the SMTP server should listen on"],
    ]

    def opt_pop3password(self,password):
        """The password used to authenticate the pop3 user"""
        if password in ('','-'):
            self['password']=util.getPassword(confirm=1)
        else:
            self['password']=password

    opt_w = opt_pop3password

    def postOptions(self):
        if not self.service.hasPassword() and not self.has_key('password'):
            self.opt_pop3password('-')
        if self.has_key('password') and self['password'] != '':
            self.service.updateCredentials(self['pop3username'],self['password'])

    def __init__(self):
        usage.Options.__init__(self)
        self.service = service.EmailService()

def makeService(config):
    internet.TCPServer(config['smtpport'],config.service.getSMTPFactory(),10,config['smtplisten']).setServiceParent(config.service)
    internet.TCPServer(config['pop3port'],config.service.getPOP3Factory(),10,config['pop3listen']).setServiceParent(config.service)
    return config.service
