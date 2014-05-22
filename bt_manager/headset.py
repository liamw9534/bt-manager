from __future__ import unicode_literals

from audio import BTAudio
from device import BTGenericDevice


class BTHeadset(BTAudio):
    """Wrapper around Dbus to encapsulate the BT headset entity"""

    SIGNAL_ANSWER_REQUESTED = 'AnswerRequested'
    SIGNAL_SPEAKER_GAIN_CHANGED = 'SpeakerGainChanged'
    SIGNAL_MICROPHONE_GAIN_CHANGED = 'MicrophoneGainChanged'

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Headset',
                                 *args, **kwargs)
        self._register_signal_name(BTHeadset.SIGNAL_ANSWER_REQUESTED)
        self._register_signal_name(BTHeadset.SIGNAL_SPEAKER_GAIN_CHANGED)
        self._register_signal_name(BTHeadset.SIGNAL_MICROPHONE_GAIN_CHANGED)

    def is_connected(self):
        return self._interface.IsConnected()

    def indicate_call(self):
        """Indicate an incoming call on the headset
        connected to the stream. Will continue to
        ring the headset about every 3 seconds."""
        return self._interface.IndicateCall()

    def cancel_call(self):
        """Cancel the incoming call indication"""
        return self._interface.CancelCall()

    def play(self):
        """Open the audio connection to the headset"""
        return self._interface.Play()

    def stop(self):
        """Close the audio connection"""
        return self._interface.Stop()


class BTHeadsetGateway(BTAudio):
    """Wrapper around Dbus to encapsulate the BT headset
    gateway entity"""

    SIGNAL_RING = 'Ring'
    SIGNAL_CALL_TERMINATED = 'CallTerminated'
    SIGNAL_CALL_STARTED = 'CallStarted'
    SIGNAL_CALL_ENDED = 'CallEnded'

    def __init__(self, *args, **kwargs):
        BTGenericDevice.__init__(self, addr='org.bluez.Headset',
                                 *args, **kwargs)
        self._register_signal_name(BTHeadsetGateway.SIGNAL_RING)
        self._register_signal_name(BTHeadsetGateway.SIGNAL_CALL_TERMINATED)
        self._register_signal_name(BTHeadsetGateway.SIGNAL_CALL_STARTED)
        self._register_signal_name(BTHeadsetGateway.SIGNAL_CALL_ENDED)

    def answer_call(self):
        """It has to called only after Ring signal received."""
        return self._interface.AnswerCall()

    def terminate_call(self):
        """Terminate call which is running or reject an incoming
        call. This has nothing with any 3-way situation incl.
        RaH. Just plain old PDH."""
        return self._interface.TerminateCall()

    def call(self, dial_number):
        """Dial a number. No number processing is done
        thus if AG would reject to dial it don't blame me"""
        return self._interface.Call(dial_number)

    def get_operator_name(self):
        """Find out the name of the currently selected network
        operator by AG."""
        return self._interface.GetOperatorName()

    def send_dtmf(self, digits):
        """Will send each digit in the 'digits' sequentially. Would
        send nothing if there is non-DTMF digit."""
        return self._interface.SendDTMF(digits)

    def get_subscriber_number(self):
        """Get the voicecall subscriber number of AG"""
        return self._interface.GetSubscriberNumber()
