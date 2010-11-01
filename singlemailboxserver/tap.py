import service
from twisted.python import usage
from twisted.application import internet

class Options(usage.Options):
    def __init__(self):
        usage.Options.__init__(self)
        self.service = service.EmailService()

def makeService(config):
    internet.TCPServer(2500,config.service.getSMTPFactory(),10,'127.0.0.1').setServiceParent(config.service)
    internet.TCPServer(1100,config.service.getPOP3Factory(),10,'127.0.0.1').setServiceParent(config.service)
    return config.service
    
        
    
