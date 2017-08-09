from flask import Flask
from flask_restful import (
    Api,
)

from raiden_mps.channel_manager import (
    ChannelManager,
    Blockchain,
)

from raiden_mps.proxy.resources import (
    Expensive,
    ChannelManagementAdmin,
    ChannelManagementClose,
    ChannelManagementRoot
)

from raiden_mps.test.utils import BlockchainMock

from raiden_mps.config import CHANNEL_MANAGER_ADDRESS


class PaymentProxy:
    config = {
        "contract_address": CHANNEL_MANAGER_ADDRESS,
        "receiver_address": "0x" + "2" * 40,
    }

    def __init__(self, blockchain):
        assert isinstance(blockchain, Blockchain) or isinstance(blockchain, BlockchainMock)
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.channel_manager = ChannelManager(
            blockchain,
            self.config['receiver_address'])

        self.api.add_resource(Expensive, '/expensive/<path:content>',
                              resource_class_kwargs={
                                  'price': 1,
                                  'contract_address': self.config['contract_address'],
                                  'receiver_address': self.config['receiver_address'],
                                  'channel_manager': self.channel_manager})

        self.api.add_resource(ChannelManagementAdmin, "/cm/admin")
        self.api.add_resource(ChannelManagementClose, "/cm/close")
        self.api.add_resource(ChannelManagementRoot, "/cm")

    def run(self, debug=False):
        self.app.run(debug=debug)
