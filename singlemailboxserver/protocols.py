from zope.interface import implements
from twisted.application import service
from twisted.internet import defer
from twisted.mail import smtp,maildir,pop3
from twisted.internet import protocol
import os



class MaildirMessageDelivery:
    implements(smtp.IMessageDelivery)

    def __init__(self,service):
        self.service = service

    def receivedHeader(self, helo, origin, recipients):
        return "Received: Maildir"
    
    def validateFrom(self,helo,origin):
        return origin

    def validateTo(self, user):
        maildirpath = self.service.maildirDirectory()
        if not os.path.exists(maildirpath):
            maildir.initializeMaildir(maildirpath)
        fname = maildir._generateMaildirName()
        filename = os.path.join(maildirpath,'tmp',fname)
        fp = open(filename,'w')
        return lambda: maildir.MaildirMessage(
            '%s@%s' % (user.dest.local, user.dest.domain), 
            fp, filename, os.path.join(maildirpath, 'new', fname))
                                      
class SMTPFactory(smtp.SMTPFactory):
    def __init__(self, service, *a, **kw):
        smtp.SMTPFactory.__init__(self, *a, **kw)
        self.delivery = MaildirMessageDelivery(service)
    
    def buildProtocol(self, addr):
        p = smtp.SMTPFactory.buildProtocol(self, addr)
        p.delivery = self.delivery
        return p

class POP3Factory(protocol.ServerFactory):
    
    portal = None

    def __init__(self,portal):
        self.portal = portal
        
    
    def buildProtocol(self,addr):
        p = pop3.POP3()
        p.portal = self.portal
        return p;

