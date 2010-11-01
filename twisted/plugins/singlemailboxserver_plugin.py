from twisted.application.service import ServiceMaker

TwistedMail = ServiceMaker(
    "Dummy Email Server",
    "singlemailboxserver.tap",
    "An email service",
    "singlemailboxserver")

