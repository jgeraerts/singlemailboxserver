from zope.interface import implements
from twisted.application import service
from twisted.cred import portal,checkers
from twisted.mail import maildir,pop3
import os
import protocols

class EmailService(service.MultiService):
    implements(portal.IRealm)

    def __init__(self):
        service.MultiService.__init__(self)
        self.portal = portal.Portal(self)
        checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
        checker.addUser("guest","password")
        self.portal.registerChecker(checker)

    def requestAvatar(self,avatarId, mind, *interfaces):
        if pop3.IMailbox in interfaces:
            return (pop3.IMailbox,maildir.MaildirMailbox(self.maildirDirectory()),None)
        raise NotImplementedError("interface not supported")

    def userDir(self):
        try:
            from win32com.shell import shellcon, shell            
            return shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
        except ImportError:
            return os.path.expanduser("~")

    def maildirDirectory(self):
        return os.path.join(self.userDir(),'Maildir')

    def getPOP3Factory(self):
        return protocols.POP3Factory(self.portal);

    def getSMTPFactory(self):
        return protocols.SMTPFactory(self)
