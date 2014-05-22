from __future__ import unicode_literals

import dbus.service
import gobject
import pprint
import os

from collections import namedtuple
from device import BTGenericDevice
from media import GenericEndpoint, BTMediaTransport
from codecs import SBCChannelMode, SBCSamplingFrequency, \
    SBCAllocationMethod, SBCSubbands, SBCBlocks, A2DP_CODECS
from serviceuuids import SERVICES
from exceptions import BTIncompatibleTransportAccessType, \
    BTInvalidConfiguration

class BTAudio(BTGenericDevice):
    """Wrapper around Dbus to encapsulate the BT audio entity"""

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Audio',
                                 *args, **kwargs)

    def connect(self):
        """Connect all supported audio profiles on the device."""
        self._interface.Connect()

    def disconnect(self):
        """Disconnect all audio profiles on the device"""
        self._interface.Disconnect()


class BTAudioSource(BTAudio):
    """Wrapper around Dbus to encapsulate the BT audio source entity"""

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.AudioSource',
                                 *args, **kwargs)


class BTAudioSink(BTAudio):
    """Wrapper around Dbus to encapsulate the BT audio sink entity"""

    SIGNAL_CONNECTED = 'Connected'
    SIGNAL_DISCONNECTED = 'Disconnected'
    SIGNAL_PLAYING = 'Playing'
    SIGNAL_STOPPED = 'Stopped'

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.AudioSink',
                                 *args, **kwargs)
        self._register_signal_name(BTAudioSink.SIGNAL_CONNECTED)
        self._register_signal_name(BTAudioSink.SIGNAL_DISCONNECTED)
        self._register_signal_name(BTAudioSink.SIGNAL_PLAYING)
        self._register_signal_name(BTAudioSink.SIGNAL_STOPPED)

    def is_connected(self):
        """Returns TRUE if a stream is setup to a A2DP sink on
        the remote device."""
        return self._interface.IsConnected()


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
            raise BTIncompatibleTransportAccessType
        return os.read(self.fd, self.write_mtu)

    def write_transport(self, data):
        """Allow user to write data to media transport"""
        if ('w' not in self.access_type):
            raise BTIncompatibleTransportAccessType
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
                # TODO: Invalid channel_mode
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
                # TODO: Invalid channel_mode
                return 51
        else:
            # TODO: Invalid frequency
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
            raise BTInvalidConfiguration

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
            raise BTInvalidConfiguration

        if ((our_caps.subbands & device_caps.subbands) &
                SBCSubbands.SUBBANDS_8):
            subbands = SBCSubbands.SUBBANDS_8
        elif ((our_caps.subbands & device_caps.subbands) &
              SBCSubbands.SUBBANDS_4):
            subbands = SBCSubbands.SUBBANDS_4
        else:
            raise BTInvalidConfiguration

        if ((our_caps.allocation_method & device_caps.allocation_method) &
                SBCAllocationMethod.LOUDNESS):
            allocation_method = SBCAllocationMethod.LOUDNESS
        elif ((our_caps.allocation_method & device_caps.allocation_method) &
              SBCAllocationMethod.SNR):
            allocation_method = SBCAllocationMethod.SNR
        else:
            raise BTInvalidConfiguration

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
                 path='/endpoint/a2dpsink'):
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
                                        BTAudioSource.SIGNAL_PROPERTY_CHANGED,  # noqa
                                        transport)


# SBCAudioSource implies the BT adapter takes on the role of source and
# the external device is the sink e.g., speaker
class SBCAudioSource(SBCAudioCodec):
    """SBC audio source media endpoint"""
    def __init__(self,
                 path='/endpoint/a2dpsource'):
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
                                      BTAudioSource.SIGNAL_PROPERTY_CHANGED,  # noqa
                                      transport)
