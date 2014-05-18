from __future__ import unicode_literals

import dbus
import dbus.service
from bt_manager import SERVICES
from bt_manager.BTCodecs import SBCAllocationMethod, SBCBlocks, \
    SBCChannelMode, SBCSamplingFrequency, SBCSubbands, A2DP_CODECS


class BTRejectedException(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


class BTAgent(dbus.service.Object):
    """Simple BT device pairing agent"""

    NOTIFY_ON_RELEASE = 'Release'
    NOTIFY_ON_AUTHORIZE = 'Authorize'
    NOTIFY_ON_REQUEST_PIN_CODE = 'RequestPinCode'
    NOTIFY_ON_REQUEST_PASS_KEY = 'RequestPasskey'
    NOTIFY_ON_DISPLAY_PASS_KEY = 'DisplayPasskey'
    NOTIFY_ON_REQUEST_CONFIRMATION = 'RequestConfirmation'
    NOTIFY_ON_CONFIRM_MODE_CHANGE = 'ConfirmModeChange'
    NOTIFY_ON_CANCEL = 'Cancel'

    def __init__(self,
                 path='/test/agent',
                 auto_authorize_connections=True,
                 default_pin_code='0000',
                 default_pass_key=0,   # Range: 0-999999
                 cb_notify_on_release=None,
                 cb_notify_on_authorize=None,
                 cb_notify_on_request_pin_code=None,
                 cb_notify_on_request_pass_key=None,
                 cb_notify_on_display_pass_key=None,
                 cb_notify_on_request_confirmation=None,
                 cb_notify_on_confirm_mode_change=None,
                 cb_notify_on_cancel=None):

        self.auto_authorize_connections = auto_authorize_connections
        self.default_pin_code = default_pin_code
        self.default_pass_key = default_pass_key
        self.cb_notify_on_release = cb_notify_on_release
        self.cb_notify_on_authorize = cb_notify_on_authorize
        self.cb_notify_on_request_pin_code = cb_notify_on_request_pin_code
        self.cb_notify_on_request_pass_key = cb_notify_on_request_pass_key
        self.cb_notify_on_display_pass_key = cb_notify_on_display_pass_key
        self.cb_notify_on_request_confirmation = \
            cb_notify_on_request_confirmation
        self.cb_notify_on_confirm_mode_change = \
            cb_notify_on_confirm_mode_change
        self.cb_notify_on_cancel = cb_notify_on_cancel
        bus = dbus.SystemBus()
        super(BTAgent, self).__init__(bus, path)

    # Service object entry points defined below here
    @dbus.service.method("org.bluez.Agent", in_signature="", out_signature="")
    def Release(self):
        if (self.cb_notify_on_release):
            self.cb_notify_on_release(BTAgent.NOTIFY_ON_RELEASE)

    @dbus.service.method("org.bluez.Agent", in_signature="os",
                         out_signature="")
    def Authorize(self, device, uuid):
        if (self.cb_notify_on_authorize):
            if (not self.cb_notify_on_authorize(BTAgent.NOTIFY_ON_AUTHORIZE,
                                                device,
                                                uuid)):
                raise BTRejectedException('Connection not authorized by user')
        elif (not self.auto_authorize_connections):
            raise BTRejectedException('Auto authorize is off')

    @dbus.service.method("org.bluez.Agent", in_signature="o",
                         out_signature="s")
    def RequestPinCode(self, device):
        if (self.cb_notify_on_request_pin_code):
            pin_code = self.cb_notify_on_request_pin_code(BTAgent.NOTIFY_ON_REQUEST_PIN_CODE,  # noqa
                                                          device)
            if (pin_code is None):
                raise BTRejectedException('User did not provide PIN code')
        elif (self.default_pin_code is None):
            raise BTRejectedException('No default PIN code set')
        else:
            pin_code = self.default_pin_code
        return dbus.String(pin_code)

    @dbus.service.method("org.bluez.Agent", in_signature="o",
                         out_signature="s")
    def RequestPasskey(self, device):
        if (self.cb_notify_on_request_pass_key):
            pass_key = self.cb_notify_on_request_pass_key(BTAgent.NOTIFY_ON_REQUEST_PASS_KEY,  # noqa
                                                          device)
            if (pass_key is None):
                raise BTRejectedException('User did not provide pass key')
        elif (self.default_pass_key is None):
            raise BTRejectedException('No default pass key set')
        else:
            pass_key = self.default_pass_key
        return dbus.UInt32(pass_key)

    @dbus.service.method("org.bluez.Agent", in_signature="ou",
                         out_signature="")
    def DisplayPasskey(self, device, pass_key):
        if (self.cb_notify_on_display_pass_key):
            self.cb_notify_on_display_pass_key(BTAgent.NOTIFY_ON_DISPLAY_PASS_KEY,  # noqa
                                               device, pass_key)

    @dbus.service.method("org.bluez.Agent", in_signature="ou",
                         out_signature="")
    def RequestConfirmation(self, device, pass_key):
        if (self.cb_notify_on_request_confirmation):
            if (not self.cb_notify_on_request_confirmation(BTAgent.NOTIFY_ON_REQUEST_CONFIRMATION,  # noqa
                                                           device, pass_key)):
                raise \
                    BTRejectedException('User confirmation of pass key negative')  # noqa

    @dbus.service.method("org.bluez.Agent", in_signature="s", out_signature="")
    def ConfirmModeChange(self, mode):
        if (self.cb_notify_on_confirm_mode_change):
            if (not self.cb_notify_on_confirm_mode_change(BTAgent.NOTIFY_ON_CONFIRM_MODE_CHANGE,  # noqa
                                                          mode)):
                raise \
                    BTRejectedException('User mode change confirmation negative')  # noqa

    @dbus.service.method("org.bluez.Agent", in_signature="", out_signature="")
    def Cancel(self):
        if (self.cb_notify_on_cancel):
            self.cb_notify_on_cancel(BTAgent.NOTIFY_ON_CANCEL)


# Can't be directly instantiated -- should be sub-classed
class GenericEndpoint(dbus.service.Object):
    def __init__(self, path):
        bus = dbus.SystemBus()
        super(GenericEndpoint, self).__init__(bus, path)

    def set_configuration(self, configuration):
        self.configuration = configuration

    def get_properties(self):
        return self.properties

    # Service object entry points defined below here
    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="", out_signature="")
    def Release(self):
        print("Release")

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="", out_signature="")
    def ClearConfiguration(self):
        print("ClearConfiguration")

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="oay", out_signature="")
    def SetConfiguration(self, transport, config):
        print("SetConfiguration (%s, %s)" % (transport, config))
        return

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="ay", out_signature="ay")
    def SelectConfiguration(self, caps):
        print("SelectConfiguration (%s)" % (caps))
        return self.configuration


class BTSBCAudioSinkEndpoint(GenericEndpoint):
    """SBC audio sink media endpoint"""
    def __init__(self,
                 default_channel_mode=SBCChannelMode.CHANNEL_MODE_JOINT_STEREO,
                 default_frequency=SBCSamplingFrequency.FREQ_44_1KHZ,
                 default_subbands=SBCSubbands.SUBBANDS_8,
                 default_allocation_method=SBCAllocationMethod.SNR,
                 default_blocks=SBCBlocks.BLOCKS_16,
                 default_min_bitpool=2,
                 default_max_bitpool=32,
                 path='test/sbcsink'):
        caps = BTSBCAudioSinkEndpoint.make_config(SBCChannelMode.ALL,
                                                  SBCSamplingFrequency.ALL,
                                                  SBCAllocationMethod.ALL,
                                                  SBCSubbands.ALL,
                                                  SBCBlocks.ALL,
                                                  2,
                                                  64)
        self.properties = dbus.Dictionary({'UUID': SERVICES['AudioSink'].uuid,
                                           'Codec': A2DP_CODECS['SBC'],
                                           'DelayReporting': True,
                                           'Capabilities': caps})
        self.set_configuration(default_channel_mode,
                               default_frequency,
                               default_allocation_method,
                               default_subbands,
                               default_blocks,
                               default_min_bitpool,
                               default_max_bitpool)
        super(BTSBCAudioSinkEndpoint, self).__init__(path)

    def set_configuration(self, channel_mode, frequency, allocation_method,
                          subbands, block_length, min_bitpool, max_bitpool):
        self.configuration = BTSBCAudioSinkEndpoint.make_config(channel_mode,
                                                                frequency,
                                                                allocation_method,  # noqa
                                                                subbands,
                                                                block_length,
                                                                min_bitpool,
                                                                max_bitpool)

    @staticmethod
    def make_config(channel_mode, frequency, allocation_method,
                    subbands, block_length, min_bitpool, max_bitpool):
        # The SBC config encoding is taken from a2dp_codecs.h, in particular,
        # the a2dp_sbc_t type:
        #   uint8_t channel_mode:4
        #   uint8_t frequency:4
        #   uint8_t allocation_method:2
        #   uint8_t subbands:2
        #   uint8_t block_length:4
        #   uint8_t min_bitpool
        #   uint8_t max_bitpool
        return dbus.Array([dbus.Byte((channel_mode << 4) | frequency),
                           dbus.Byte((allocation_method << 6) |
                                     (subbands << 4) | block_length),
                           dbus.Byte(min_bitpool),
                           dbus.Byte(max_bitpool)])
