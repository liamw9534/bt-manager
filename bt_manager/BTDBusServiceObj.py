from __future__ import unicode_literals
from collections import namedtuple

import dbus
import dbus.service
import pprint
import gobject
import os
from bt_manager import SERVICES, BTMediaTransport, BTAudioSource, \
    BTAudioSink
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


# GenericEndpoint can't be directly instantiated.  It should be
# sub-classed and provides a template class only.
class GenericEndpoint(dbus.service.Object):
    def __init__(self, path):
        bus = dbus.SystemBus()
        super(GenericEndpoint, self).__init__(bus, path)

    def get_properties(self):
        """Returns the properties of the endpoint -- these should
        be initialized by a suitable subclass implementation"""
        return self.properties

    # Service object entry points defined below here --
    # you will need to implement these in your subclass
    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="", out_signature="")
    def Release(self):
        """Called by bluez to let us know our registration
        has been released - the endpoint no longer exists"""
        pass

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="", out_signature="")
    def ClearConfiguration(self):
        """Called by bluez to let us know that the audio
        streaming process has been reset, for whatever reason, and
        we should clean-up."""
        pass

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="oay", out_signature="")
    def SetConfiguration(self, transport, config):
        """Provides a path to the media transport to use and the active
        configuration that has been negotiated."""
        pass

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="ay", out_signature="ay")
    def SelectConfiguration(self, caps):
        """Initiates negotiations of the capabilities"""
        pass


SBCCodecConfig = namedtuple('SBCCodecConfig',
                            'channel_mode frequency allocation_method '
                            'subbands block_length min_bitpool '
                            'max_bitpool')


# SBCAudioCodec does not implement RTP pay/depay or SBC encode/decode.
# It only implements the necessary parts for creating the media endpoint,
# negotiating the connection and establishing a media transport.
class SBCAudioCodec(GenericEndpoint):

    def __init__(self, uuid, path):
        config = SBCCodecConfig(SBCChannelMode.ALL,
                                SBCSamplingFrequency.ALL,
                                SBCAllocationMethod.ALL,
                                SBCSubbands.ALL,
                                SBCBlocks.ALL,
                                2,
                                64)
        caps = SBCAudioCodec._make_config(config)
        codec = dbus.Byte(A2DP_CODECS['SBC'])
        delayed_reporting = dbus.Boolean(True)
        self.properties = dbus.Dictionary({'UUID': uuid,
                                           'Codec': codec,
                                           'DelayReporting': delayed_reporting,
                                           'Capabilities': caps})
        GenericEndpoint.__init__(self, path)

    def read_transport(self):
        """Allow user to read data from media transport"""
        if ('r' not in self.access_type):
            return
        return os.read(self.fd, self.write_mtu)

    def write_transport(self, data):
        """Allow user to write data to media transport"""
        if ('w' not in self.access_type):
            return
        os.write(self.fd, data)

    def _notify_media_transport_available(self, path, transport):
        """Subclass should implement this to trigger setup once
        a new media transport is available."""
        pass

    def _acquire_media_transport(self, path, access_type):
        """Should be called by subclass when it is ready
        to acquire the media transport file descriptor"""
        transport = BTMediaTransport(path=path)
        (fd, write_mtu, read_mtu) = transport.acquire(access_type)
        self.fd = fd.take()   # We must do the clean-up later
        self.write_mtu = write_mtu
        self.read_mtu = read_mtu
        self.access_type = access_type

    def _release_media_transport(self, path, access_type):
        """Should be called by subclass when it is finished
        with the media transport file descriptor"""
        os.close(self.fd)   # Clean-up previously taken fd
        transport = BTMediaTransport(path=path)
        transport.release(access_type)

    @staticmethod
    def _default_bitpool(frequency, channel_mode):
        if (frequency ==
                SBCSamplingFrequency.FREQ_16KHZ or
            frequency ==
                SBCSamplingFrequency.FREQ_32KHZ):
            return 53
        elif (frequency ==
                SBCSamplingFrequency.FREQ_44_1KHZ):
            if (channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_MONO or
                channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_DUAL):
                return 31
            elif (channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_STEREO or
                  channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_JOINT_STEREO):
                return 53
            else:
                print('Invalid channel_mode')
                return 53
        elif (frequency == SBCSamplingFrequency.FREQ_48KHZ):
            if (channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_MONO or
                channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_DUAL):
                return 29
            elif (channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_STEREO or
                  channel_mode ==
                    SBCChannelMode.CHANNEL_MODE_JOINT_STEREO):
                return 51
            else:
                print('Invalid channel_mode')
                return 51
        else:
            print('Invalid frequency')
            return 53

    @staticmethod
    def _make_config(config):
        """Helper to turn SBC codec configuration params into a
        a2dp_sbc_t structure usable by bluez"""
        # The SBC config encoding is taken from a2dp_codecs.h, in particular,
        # the a2dp_sbc_t type is converted into a 4-byte array:
        #   uint8_t channel_mode:4
        #   uint8_t frequency:4
        #   uint8_t allocation_method:2
        #   uint8_t subbands:2
        #   uint8_t block_length:4
        #   uint8_t min_bitpool
        #   uint8_t max_bitpool
        return dbus.Array([dbus.Byte(config.channel_mode |
                                     (config.frequency << 4)),
                           dbus.Byte(config.allocation_method |
                                     (config.subbands << 2) |
                                     (config.block_length << 4)),
                           dbus.Byte(config.min_bitpool),
                           dbus.Byte(config.max_bitpool)])

    @staticmethod
    def _parse_config(config):
        """Helper to turn a2dp_sbc_t structure into a
        more usable set of SBC codec configuration params"""
        frequency = config[0] >> 4
        channel_mode = config[0] & 0xF
        allocation_method = config[1] & 0x03
        subbands = (config[1] >> 2) & 0x03
        block_length = (config[1] >> 4) & 0x0F
        min_bitpool = config[2]
        max_bitpool = config[3]
        return SBCCodecConfig(channel_mode, frequency, allocation_method,
                              subbands, block_length, min_bitpool, max_bitpool)

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="", out_signature="")
    def Release(self):
        print('Release')

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="", out_signature="")
    def ClearConfiguration(self):
        print('ClearConfiguration')

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="ay", out_signature="ay")
    def SelectConfiguration(self, caps):
        print('SelectConfiguration(%s)' % caps)
        our_caps = SBCAudioCodec._parse_config(self.properties['Capabilities'])
        device_caps = SBCAudioCodec._parse_config(caps)
        frequency = SBCSamplingFrequency.FREQ_44_1KHZ

        if ((our_caps.channel_mode & device_caps.channel_mode) &
                SBCChannelMode.CHANNEL_MODE_JOINT_STEREO):
            channel_mode = SBCChannelMode.CHANNEL_MODE_JOINT_STEREO
        elif ((our_caps.channel_mode & device_caps.channel_mode) &
              SBCChannelMode.CHANNEL_MODE_STEREO):
            channel_mode = SBCChannelMode.CHANNEL_MODE_STEREO
        elif ((our_caps.channel_mode & device_caps.channel_mode) &
              SBCChannelMode.CHANNEL_MODE_DUAL):
            channel_mode = SBCChannelMode.CHANNEL_MODE_DUAL
        elif ((our_caps.channel_mode & device_caps.channel_mode) &
              SBCChannelMode.CHANNEL_MODE_MONO):
            channel_mode = SBCChannelMode.CHANNEL_MODE_MONO
        else:
            print('Unable to set channel_mode')

        if ((our_caps.block_length & device_caps.block_length) &
                SBCBlocks.BLOCKS_16):
            block_length = SBCBlocks.BLOCKS_16
        elif ((our_caps.block_length & device_caps.block_length) &
              SBCBlocks.BLOCKS_12):
            block_length = SBCBlocks.BLOCKS_12
        elif ((our_caps.block_length & device_caps.block_length) &
              SBCBlocks.BLOCKS_8):
            block_length = SBCBlocks.BLOCKS_8
        elif ((our_caps.block_length & device_caps.block_length) &
              SBCBlocks.BLOCKS_4):
            block_length = SBCBlocks.BLOCKS_4
        else:
            print('Unable to set block_length')

        if ((our_caps.subbands & device_caps.subbands) &
                SBCSubbands.SUBBANDS_8):
            subbands = SBCSubbands.SUBBANDS_8
        elif ((our_caps.subbands & device_caps.subbands) &
              SBCSubbands.SUBBANDS_4):
            subbands = SBCSubbands.SUBBANDS_4
        else:
            print('Unable to set subbands')

        if ((our_caps.allocation_method & device_caps.allocation_method) &
                SBCAllocationMethod.LOUDNESS):
            allocation_method = SBCAllocationMethod.LOUDNESS
        elif ((our_caps.allocation_method & device_caps.allocation_method) &
              SBCAllocationMethod.SNR):
            allocation_method = SBCAllocationMethod.SNR
        else:
            print('Unable to set allocation_method')

        min_bitpool = max(our_caps.min_bitpool, device_caps.min_bitpool)
        max_bitpool = min(SBCAudioCodec._default_bitpool(frequency,
                                                         channel_mode),
                          device_caps.max_bitpool)

        selected_config = SBCCodecConfig(channel_mode,
                                         frequency,
                                         allocation_method,
                                         subbands,
                                         block_length,
                                         min_bitpool,
                                         max_bitpool)
        dbus_val = SBCAudioCodec._make_config(selected_config)
        return dbus_val

    @dbus.service.method("org.bluez.MediaEndpoint",
                         in_signature="oay", out_signature="")
    def SetConfiguration(self, transport, config):
        print('SetConfiguration(%s, %s)' % (transport, config))
        self._notify_media_transport_available(config.get('Device'), transport)

    def __repr__(self):
        return pprint.pformat(self.__dict__)


# SBCAudioSink implies the BT adapter takes on the role of a sink and
# the external device is the source e.g., iPhone, media player
class SBCAudioSink(SBCAudioCodec):
    """SBC audio sink media endpoint"""
    def __init__(self,
                 path='test/sbcsink'):
        uuid = dbus.String(SERVICES['AudioSink'].uuid)
        SBCAudioCodec.__init__(self, uuid, path)

    def _fd_ready_handler(self, fd, cb_condition):
        """Wrapper for calling user callback routine to notify
        when transport data is ready to read"""
        self.user_cb(fd, self.user_arg)
        return True

    def register_fd_ready_event(self, user_cb, user_arg):
        """Register for fd ready events"""
        self.user_cb = user_cb
        self.user_arg = user_arg
        self.tag = gobject.io_add_watch(self.fd, gobject.IO_IN,
                                        self._fd_ready_handler)

    def unregister_fd_ready_event(self):
        """Unregister fd ready events"""
        gobject.source_remove(self.tag)

    def _property_change_event_handler(self, signal, transport, *args):
        """Handler for property change event.  We catch certain state
        transitions in order to trigger media transport
        acquisition/release"""
        current_state = self.source.State
        if (self.state == 'connected' and current_state == 'playing'):
            self._acquire_media_transport(transport, 'r')
        elif (self.state == 'playing' and current_state == 'connected'):
            self._release_media_transport(transport, 'r')
        self.state = current_state

    def _notify_media_transport_available(self, path, transport):
        """Called by the endpoint when a new media transport is
        available"""
        self.source = BTAudioSource(dev_path=path)
        self.state = self.source.State
        self.source.add_signal_receiver(self._property_change_event_handler,
                                        BTAudioSource.SIGNAL_PROPERTY_CHANGED,
                                        transport)


# SBCAudioSource implies the BT adapter takes on the role of source and
# the external device is the sink e.g., speaker
class SBCAudioSource(SBCAudioCodec):
    """SBC audio source media endpoint"""
    def __init__(self,
                 path='test/sbcsource'):
        uuid = dbus.String(SERVICES['AudioSource'].uuid)
        SBCAudioCodec.__init__(self, uuid, path)

    def _property_change_event_handler(self, signal, transport, *args):
        """Handler for property change event.  We catch certain state
        transitions in order to trigger media transport
        acquisition/release"""
        current_state = self.sink.State
        if ((self.state == 'disconnected' and current_state == 'connected') or
            (self.state == 'connecting' and
                current_state == 'connected')):
            self._acquire_media_transport(transport, 'w')
        elif (self.state == 'connected' and current_state == 'disconnected'):
            self._release_media_transport(transport, 'w')
        self.state = current_state

    def _notify_media_transport_available(self, path, transport):
        """Called by the endpoint when a new media transport is
        available"""
        self.sink = BTAudioSink(dev_path=path)
        self.state = self.sink.State
        self.sink.add_signal_receiver(self._property_change_event_handler,
                                      BTAudioSource.SIGNAL_PROPERTY_CHANGED,
                                      transport)
