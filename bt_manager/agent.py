from __future__ import unicode_literals

import dbus.service

from exceptions import BTRejectedException


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
