from __future__ import unicode_literals

__SupportedFeatureOnly = {
    '0311': 'SupportedFeatures',
}

__BIP = {
    '0311': 'SupportedFeatures',
    '0200': 'GoepL2capPsm',
    '0310': 'SupportedCapabilities',
    '0312': 'SupportedFunctions',
    '0313': 'TotalImagingDataCapacity',
}

__BPP = {
    '0350': 'Document Formats Supported',
    '0352': 'Character Repertoires Supported',
    '0354': 'XHTML-Print Image Formats Supported',
    '0356': 'Color Supported',
    '0358': '1284ID',
    '035A': 'Printer Name',
    '035C': 'Printer Location',
    '035E': 'Duplex Supported',
    '0360': 'Media Types Supported',
    '0362': 'MaxMediaWidth',
    '0364': 'MaxMediaLength',
    '0366': 'Enhanced Layout Supported',
    '0368': 'RUI Formats Supported',
    '0370': 'Reference Printing RUI Supported',
    '0372': 'Direct Printing RUI Supported',
    '0374': 'Reference Printing Top URL',
    '0376': 'Direct Printing Top URL',
    '0378': 'Printer Admin RUI Top URL',
    '037A': 'Device Name',
}

__Universal = {
    '0000': 'ServiceRecordHandle',
    '0001': 'ServiceClassIDList',
    '0002': 'ServiceRecordState',
    '0003': 'ServiceID',
    '0004': 'ProtocolDescriptorList',
    '0005': 'BrowseGroupList',
    '0006': 'LanguageBaseAttributeIDList',
    '0007': 'ServiceInfoTimeToLive',
    '0008': 'ServiceAvailability',
    '0009': 'BluetoothProfileDescriptorList',
    '000A': 'DocumentationURL',
    '000B': 'ClientExecutableURL',
    '000C': 'IconURL',
    '000D': 'AdditionalProtocolDescriptorLists',
}

__ServiceDiscoveryService = {
    '0200': 'VersionNumberList',
    '0201': 'ServiceDatabaseState',
}

__BrowseGroupDescriptorService = {
    '0200': 'GroupID',
}

__CordlessTelephony = {
    '0301': 'External Network',
}

__DeviceIdentification = {
    '0200': 'SpecificationID',
    '0201': 'VendorID',
    '0202': 'ProductID',
    '0203': 'Version',
    '0204': 'PrimaryRecord',
    '0205': 'VendorIDSource',
}

__Fax = {
    '0302': 'Fax Class 1 Support',
    '0303': 'Fax Class 2.0 Support',
    '0304': 'Fax Class 2 Support(vendor-specific class)',
    '0305': 'Audio Feedback Support',
}

__FTP = {
    '0200': 'GoepL2capPsm(FTP v1.2 and later)',
}

__GNSSService = {
    '0200': 'SupportedFeatures'
}

__HandsFreeProfile = {
    '0301': 'Network',
    '0311': 'SupportedFeatures',
}

__HardcopyReplacementProfile = {
    '0300': '1284ID',
    '0302': 'Device Name',
    '0304': 'Friendly Name',
    '0306': 'Device Location',
}

__HeadsetProfile = {
    '0302': 'Remote Audio Volume Control',
}

__HealthDeviceProfile = {
    '0200': 'SupportFeaturesList',
    '0301': 'DataExchangeSpecification',
    '0302': 'MCAP Supported Procedures',
}

__HIDProfile = {
    '0200': 'HIDDeviceReleaseNumber (Depreciated)',
    '0201': 'HIDParserVersion',
    '0202': 'HIDDeviceSubclass',
    '0203': 'HIDCountryCode',
    '0204': 'HIDVirtualCable',
    '0205': 'HIDReconnectInitiate',
    '0206': 'HIDDescriptorList',
    '0207': 'HIDLANGIDBaseList',
    '0208': 'HIDSDPDisable (Depreciated)',
    '0209': 'HIDBatteryPower',
    '020A': 'HIDRemoteWake',
    '020B': 'HIDProfileVersion',
    '020C': 'HIDSupervisionTimeout',
    '020D': 'HIDNormallyConnectable',
    '020E': 'HIDBootDevice',
    '020F': 'HIDSSRHostMaxLatency',
    '0210': 'HIDSSRHostMinTimeout',
}

__WAPBearer = {
    '0306': 'NetworkAddress',
    '0307': 'WAPGateway',
    '0308': 'HomePageURL',
    '0309': 'WAPStackType',
}

__MessageAccessProfile = {
    '0200': 'GoepLcapPsm',
    '0315': 'MASInstanceID',
    '0316': 'SupportedMessageTypes',
    '0317': 'MapSupportedFeatures',
}

__ObjectPushProfile = {
    '0200': 'GoepL2capPsm',
    '0300': 'Service Version',
    '0303': 'Supported Formats List',
}

__PANProfile = {
    '0200': 'IpSubnet',
    '030A': 'SecurityDescription',
    '030B': 'NetAccessType',
    '030C': 'MaxNetAccessrate',
    '030D': 'IPv4Subnet',
    '030E': 'IPv4Subnet',
}

__PhoneBookAccessProfile = {
    '0200': 'GoepL2capPsm',
    '0314': 'SupportedRepositories',
    '0317': 'PbapSupportedFeatures',
}

__SyncProfile = {
    '0301': 'Supported Data Stores List',
}

__MultiProfile = {
    '0200': 'MPSD Scenarios',
    '0201': 'MPMD Scenarios',
    '0202': 'Supported Profiles & Protocols',
}

ATTRIBUTES = {
    '*': __Universal,
    '110A': __SupportedFeatureOnly,
    '110B': __SupportedFeatureOnly,
    '110C': __SupportedFeatureOnly,
    '110E': __SupportedFeatureOnly,
    '110F': __SupportedFeatureOnly,
    '111B': __BIP,
    '111C': __BIP,
    '111D': __BIP,
    '1118': __BPP,
    '1119': __BPP,
    '1120': __BPP,
    '1121': __BPP,
    '1123': __BPP,
    '1000': __ServiceDiscoveryService,
    '1001': __BrowseGroupDescriptorService,
    '1200': __DeviceIdentification,
    '1111': __Fax,
    '1109': __FTP,
    '1136': __GNSSService,
    '111E': __HandsFreeProfile,
    '111F': __HandsFreeProfile,
    '1126': __HardcopyReplacementProfile,
    '1127': __HardcopyReplacementProfile,
    '1108': __HeadsetProfile,
    '1112': __HeadsetProfile,
    '1131': __HeadsetProfile,
    '1401': __HealthDeviceProfile,
    '1402': __HealthDeviceProfile,
    '1124': __HIDProfile,
    '1113': __WAPBearer,
    '1114': __WAPBearer,
    '1132': __MessageAccessProfile,
    '1133': __MessageAccessProfile,
    '1105': __ObjectPushProfile,
    '1115': __PANProfile,
    '1116': __PANProfile,
    '1117': __PANProfile,
    '112E': __PhoneBookAccessProfile,
    '112F': __PhoneBookAccessProfile,
    '1104': __SyncProfile,
    '113B': __MultiProfile,
}
