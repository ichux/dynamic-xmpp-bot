import logging

from sleekxmpp import ClientXMPP

from  inbetween import pull_data


# from sleekxmpp.exceptions import IqError, IqTimeout


# noinspection PyMethodMayBeStatic
class EchoBot(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')

        # If you are working with an OpenFire server, you will
        # need to use a different SSL version:
        # import ssl
        # self.ssl_version = ssl.PROTOCOL_SSLv3

    def session_start(self, event):
        self.send_presence(pstatus="Send me a message", pnick="Admin Bot")
        self.get_roster()

        # Most get_*/set_* methods from plugins use Iq stanzas, which
        # can generate IqError and IqTimeout exceptions
        #
        # try:
        #     self.get_roster()
        # except IqError as err:
        #     logging.error('There was an error getting the roster')
        #     logging.error(err.iq['error']['condition'])
        #     self.disconnect()
        # except IqTimeout:
        #     logging.error('Server is taking too long to respond')
        #     self.disconnect()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()
            """
            result = "utc: {0}\n".format(utc())
            result += "%(body)s" % msg

            print(msg["from"], msg["body"])  # outputs the main body
            msg.reply(result).send()
            """
            try:
                msg.reply("{}".format(pull_data(msg["body"]))).send()
            except ValueError, e:
                msg.reply("{}".format(e)).send()
            except AttributeError, e:
                msg.reply("{}".format(e)).send()


if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    # xmpp = EchoBot('admin@192.168.56.151/virtualbox', 'password')
    # xmpp = EchoBot('admin@tigase', 'tigase')
    # xmpp = EchoBot('ichux@192.168.56.152/virtualbox', 'passw0rd')
    # xmpp = EchoBot('moderator@tigase', 'passw0rd')

    xmpp = EchoBot('bot@192.168.56.151/virtualbox', 'tellnoone')
    xmpp.connect()
    xmpp.process(block=True)
