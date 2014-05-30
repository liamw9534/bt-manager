from __future__ import unicode_literals

import readline  # noqa
import bt_manager
import sys
import dbus
import dbus.mainloop.glib
import gobject
import signal
from collections import namedtuple


def dump_signal(signal, *args):
    print '\n========================================================='
    print '>>>>>', signal, '<<<<<'
    print args
    print '========================================================='


def agent_event_handler(*args):
    print '\n========================================================='
    print 'Agent event:', args
    return True


def device_created_ok(*args):
    print '\n========================================================='
    print 'New Device Paired:', args


def device_created_error(*args):
    print '\n========================================================='
    print 'Pairing Error:', args


def cmd_help(args):
    global cmd_table

    if (len(args)):
        cmd_list = [args.pop(0)]
    else:
        cmd_list = cmd_table.keys()

    for i in cmd_list:
        print i, cmd_table[i].args, ":", cmd_table[i].desc


def list_adapters(args):
    print '========================================================='
    try:
        print bt_manager.BTManager().list_adapters()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def list_devices(args):
    print '========================================================='
    global adapter

    try:
        print adapter.list_devices()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def adapter_info(args):
    global adapter

    try:
        print '========================================================='
        print adapter
        print '========================================================='
        cod = bt_manager.BTCoD(adapter.Class)
        print 'Vendor Name:', bt_manager.VENDORS.get(adapter.Vendor, 'Unknown')
        print 'Device Class:', hex(adapter.Class)
        print 'Major Service Class:', str(cod.major_service_class)
        print 'Major Device Class:', str(cod.major_device_class)
        print 'Minor Device Class:', str(cod.minor_device_class)
        print '========================================================='
        uuids = adapter.UUIDs
        for i in uuids:
            uuid = bt_manager.BTUUID(i)
            print bt_manager.SERVICES.get(uuid.uuid16, uuid)
        print '========================================================='
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def adapter_get(args):
    if (len(args)):
        name = args.pop(0)
    else:
        name = None

    print '========================================================='
    global adapter

    try:
        print adapter.get_property(name=name)
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def adapter_set(args):
    if (len(args) >= 2):
        name = args.pop(0)
        value = args.pop(0)
    else:
        print 'Error: Requires property name and value'
        return

    global adapter

    try:
        adapter.set_property(name, value)
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def device_rm(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Requires device path'
        return

    global adapter

    try:
        adapter.remove_device(dev_path)
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def device_get(args):
    if (len(args)):
        dev_path = args.pop(0)
        if (len(args)):
            name = args.pop(0)
        else:
            name = None
    else:
        print 'Error: Requires device path'
        return

    try:
        device = bt_manager.BTDevice(dev_path=dev_path)
        print '========================================================='
        print device.get_property(name=name)
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def device_set(args):
    if (len(args) >= 2):
        dev_path = args.pop(0)
        name = args.pop(0)
        value = args.pop(0)
    else:
        print 'Error: Requires device path, property name and value'
        return

    try:
        device = bt_manager.BTDevice(dev_path=dev_path)
        device.set_property(name, value)
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def device_info(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        device = bt_manager.BTDevice(dev_path=dev_path)
        print '========================================================='
        print device
        print '========================================================='
        cod = bt_manager.BTCoD(device.Class)
        print 'Vendor Name:', bt_manager.VENDORS.get(device.Vendor, 'Unknown')
        print 'Device Class:', hex(device.Class)
        print 'Major Service Class:', str(cod.major_service_class)
        print 'Major Device Class:', str(cod.major_device_class)
        print 'Minor Device Class:', str(cod.minor_device_class)
        print '========================================================='
        uuids = device.UUIDs
        for i in uuids:
            uuid = bt_manager.BTUUID(i)
            print bt_manager.SERVICES.get(uuid.uuid16, uuid)
        print '========================================================='
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def device_disconnect(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        device = bt_manager.BTDevice(dev_path=dev_path)
        device.disconnect()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def device_discovery(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        device = bt_manager.BTDevice(dev_path=dev_path)
        discovery = device.discover_services()
        if (discovery):
            for rec in discovery.keys():
                print '========================================================='  # noqa
                print bt_manager.BTDiscoveryInfo(discovery[rec])
        print '========================================================='
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def discovery_start(args):

    global adapter

    try:
        adapter.start_discovery()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def discovery_stop(args):

    global adapter

    try:
        adapter.stop_discovery()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def agent_start(args):

    global services, adapter
    dev_id = None

    if (len(args)):
        path = args.pop(0)
        if (len(args)):
            dev_id = args.pop(0)
    else:
        print 'Error: Must provide agent path e.g., /test/agent'
        return

    try:
        agent = bt_manager.BTAgent(path=path,
                                   cb_notify_on_release=agent_event_handler,
                                   cb_notify_on_authorize=agent_event_handler,
                                   cb_notify_on_request_confirmation=agent_event_handler,  # noqa
                                   cb_notify_on_confirm_mode_change=agent_event_handler,   # noqa
                                   cb_notify_on_cancel=agent_event_handler)
        services[path] = agent
        caps = 'DisplayYesNo'

        if (dev_id):
            adapter.create_paired_device(dev_id, path, caps,
                                         device_created_ok,
                                         device_created_error)
        else:
            adapter.register_agent(path, caps)
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def agent_stop(args):

    global agent, services

    if (len(args)):
        path = args.pop(0)
    else:
        print 'Error: Must provide agent path e.g., /test/agent'
        return

    try:
        adapter.unregister_agent(path)
        services[path].remove_from_connection()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def exit_cleanup(args):
    sys.exit(0)


def sink_info(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        sink = bt_manager.BTAudioSink(dev_path=dev_path)
        print '========================================================='
        print sink
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def sink_connect(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        sink = bt_manager.BTAudioSink(dev_path=dev_path)
        sink.connect()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def sink_disconnect(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        sink = bt_manager.BTAudioSink(dev_path=dev_path)
        sink.disconnect()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def source_info(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        source = bt_manager.BTAudioSource(dev_path=dev_path)
        print '========================================================='
        print source
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def source_connect(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        source = bt_manager.BTAudioSource(dev_path=dev_path)
        source.connect()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def source_disconnect(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        source = bt_manager.BTAudioSource(dev_path=dev_path)
        source.disconnect()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def control_info(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        ctrl = bt_manager.BTControl(dev_path=dev_path)
        print '========================================================='
        print ctrl
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def control_vol_up(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        ctrl = bt_manager.BTControl(dev_path=dev_path)
        ctrl.volume_up()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def control_vol_down(args):
    if (len(args)):
        dev_path = args.pop(0)
    else:
        print 'Error: Must specify device path'
        return

    try:
        ctrl = bt_manager.BTControl(dev_path=dev_path)
        ctrl.volume_down()
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def media_sbc_sink_start(args):

    global services

    if (len(args)):
        path = args.pop(0)
    else:
        print 'Error: Must provide endpoint path e.g., /test/endpoint/sbc0'
        return

    try:
        ep = bt_manager.SBCAudioSink(path=path)
        print '========================================================='
        print repr(ep)
        services[path] = ep
        media = bt_manager.BTMedia()
        media.register_endpoint(path, ep.get_properties())
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def media_decode_handler(args):
    ep = args[0]
    fd = args[1]
    data = ep.read_transport()
    fd.write(data)


def media_encode_handler(args):
    ep = args[0]
    fd = args[1]
    data = fd.read(2560)
    ep.write_transport(data)


def media_decode(args):

    global services

    if (len(args) >= 2):
        path = args.pop(0)
        filename = args.pop(0)
    else:
        print 'Error: Must provide endpoint path e.g., /test/endpoint/sbc0 and audio storage filename'  # noqa
        return

    fd = open(filename, 'wb+')
    ep = services[path]
    ep.register_transport_ready_event(media_decode_handler, (ep, fd))


def media_encode(args):

    global services

    if (len(args) >= 2):
        path = args.pop(0)
        filename = args.pop(0)
    else:
        print 'Error: Must provide endpoint path e.g., /test/endpoint/sbc0 and audio storage filename'  # noqa
        return

    fd = open(filename, 'rb')
    ep = services[path]
    ep.register_transport_ready_event(media_encode_handler, (ep, fd))


def media_sbc_source_start(args):

    global services

    if (len(args)):
        path = args.pop(0)
    else:
        print 'Error: Must provide endpoint path e.g., /test/endpoint/sbc0'
        return

    try:
        ep = bt_manager.SBCAudioSource(path=path)
        print '========================================================='
        print repr(ep)
        services[path] = ep
        media = bt_manager.BTMedia()
        media.register_endpoint(path, ep.get_properties())
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


def media_stop(args):

    global services

    if (len(args)):
        path = args.pop(0)
    else:
        print 'Error: Must provide endpoint path e.g., /test/endpoint/sbc0'
        return

    try:
        ep = services[path]
        ep.unregister_transport_ready_event()
        ep.close_transport()
        ep.remove_from_connection()
        media = bt_manager.BTMedia()
        media.unregister_endpoint(path)
    except dbus.exceptions.DBusException:
        print 'Unable to complete:', sys.exc_info()


CmdEntry = namedtuple('CmdEntry', 'func desc args')
cmd_table = {'help': CmdEntry(cmd_help,
                              'Display a list of commands or get help for a specific command',  # noqa
                              '[command]'),
             'list-adapters': CmdEntry(list_adapters,
                                       'Provide a list of available BT adapters',  # noqa
                                       None),
             'list-devices': CmdEntry(list_devices,
                                      'Display a list of paired BT devices',
                                      None),
             'adapter-info': CmdEntry(adapter_info,
                                      'Display information about default BT adapter',  # noqa
                                      None),
             'adapter-get': CmdEntry(adapter_get,
                                     'Get adapter property by name',
                                     '<property>'),
             'adapter-set': CmdEntry(adapter_set,
                                     'Set adapter property by name, value',
                                     '<property> <value>'),
             'device-rm': CmdEntry(device_rm,
                                   'Remove device from adapter',
                                   '<dev_path>'),
             'device-get': CmdEntry(device_get,
                                     'Get device property by name',
                                     '<dev_path> <property>'),
             'device-set': CmdEntry(device_set,
                                     'Set device property by name, value',
                                     '<dev_path> <property> <value>'),
             'device-info': CmdEntry(device_info,
                                     'Display information about a paired BT device',  # noqa
                                     '<dev_path>'),
             'device-disconnect': CmdEntry(device_disconnect,
                                           'Disconnect a BT device',
                                           '<dev_path>'),
             'device-discovery': CmdEntry(device_discovery,
                                          'Run BT device discovery session',
                                          '<dev_path>'),
             'discovery-start': CmdEntry(discovery_start,
                                         'Start device discovery',
                                         None),
             'discovery-stop': CmdEntry(discovery_stop,
                                        'Stop device discovery',
                                        None),
             'agent-start': CmdEntry(agent_start,
                                     'Start pairing agent',
                                     '<agent_path> [dev_id e.g., 11:22:33:44:55:66]'),  # noqa
             'agent-stop': CmdEntry(agent_stop,
                                   'Stop pairing agent',
                                   '<agent_path>'),
             'sink-info': CmdEntry(sink_info,
                                   'Audio sink properties',
                                   '<dev_path>'),
             'sink-connect': CmdEntry(sink_connect,
                                      'Audio sink connect',
                                      '<dev_path>'),
             'sink-disconnect': CmdEntry(sink_disconnect,
                                         'Audio sink connect',
                                         '<dev_path>'),
             'source-info': CmdEntry(source_info,
                                   'Audio source properties',
                                   '<dev_path>'),
             'source-connect': CmdEntry(source_connect,
                                        'Audio source connect',
                                        '<dev_path>'),
             'source-disconnect': CmdEntry(source_disconnect,
                                           'Audio source connect',
                                           '<dev_path>'),
             'control-info': CmdEntry(control_info,
                                      'Control device info',
                                      '<dev_path>'),
             'control-vol-up': CmdEntry(control_vol_up,
                                        'Control volume up',
                                        '<dev_path>'),
             'control-vol-down': CmdEntry(control_vol_down,
                                          'Control volume down',
                                          '<dev_path>'),
             'media-sbc-sink-start': CmdEntry(media_sbc_sink_start,
                                              'Start media endpoint for SBC audio sink (i.e., connects to a source device)',  # noqa
                                              '<endpoint_path>'),
             'media-decode': CmdEntry(media_decode,
                                      'Start media decode for SBC audio sink',
                                      '<endpoint_path> <audio_filename>'),
             'media-encode': CmdEntry(media_encode,
                                      'Start media encode for SBC audio source',  # noqa
                                      '<endpoint_path> <audio_filename>'),
             'media-sbc-source-start': CmdEntry(media_sbc_source_start,
                                                'Start media endpoint for SBC audio source (i.e., connects to a sink device)',  # noqa
                                                '<endpoint_path>'),
             'media-stop': CmdEntry(media_stop,
                                    'Stop media endpoint',
                                    '<endpoint_path>'),
             'exit': CmdEntry(exit_cleanup,
                              'Cleanup and exit',
                              None),
             }


def invoke_bt_command(text):
    if (not text):
        return
    args = text.split(' ')
    cmd = args.pop(0)
    cmd_entry = cmd_table.get(cmd)
    if (cmd_entry):
        cmd_entry.func(args)
    else:
        print 'Error: Command "%s" was not recognized.' % cmd


def timeout_handler(signum, frame):
    while gobject.MainLoop().get_context().pending():
        gobject.MainLoop().get_context().iteration(False)


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
gobject.threads_init()
signal.signal(signal.SIGALRM, timeout_handler)
signal.setitimer(signal.ITIMER_REAL, 0.01, 0.01)

try:
    adapter = bt_manager.BTAdapter()
    adapter.add_signal_receiver(dump_signal,
                                bt_manager.BTAdapter.SIGNAL_DEVICE_CREATED,
                                None)
    adapter.add_signal_receiver(dump_signal,
                                bt_manager.BTAdapter.SIGNAL_DEVICE_REMOVED,
                                None)
    adapter.add_signal_receiver(dump_signal,
                                bt_manager.BTAdapter.SIGNAL_DEVICE_DISAPPEARED,
                                None)
    adapter.add_signal_receiver(dump_signal,
                                bt_manager.BTAdapter.SIGNAL_DEVICE_FOUND,
                                None)
    adapter.add_signal_receiver(dump_signal,
                                bt_manager.BTAdapter.SIGNAL_PROPERTY_CHANGED,
                                None)
except dbus.exceptions.DBusException:
    print 'Unable to complete:', sys.exc_info()

services = {}

# Main command processing loop
while True:
    text = raw_input("BT> ")
    invoke_bt_command(text)
