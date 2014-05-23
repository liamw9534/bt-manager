from __future__ import unicode_literals
from collections import namedtuple

A2DP_CODECS = {'SBC': 0x00,
               'MPEG12': 0x01,
               'MPEG24': 0x02,
               'ATRAC': 0x03,
               }
"""
Enumeration of codec types supported by A2DP profile
"""

SBCCodecConfig = namedtuple('SBCCodecConfig',
                            'channel_mode frequency allocation_method '
                            'subbands block_length min_bitpool '
                            'max_bitpool')
"""
Named tuple collection of SBC A2DP audio profile properties
"""


class SBCSamplingFrequency:
    """Indicates with which sampling frequency the SBC
    frame has been encoded."""
    FREQ_16KHZ = (1 << 3)
    FREQ_32KHZ = (1 << 2)
    FREQ_44_1KHZ = (1 << 1)
    FREQ_48KHZ = 1
    ALL = 0xF


class SBCBlocks:
    """The block size with which the stream has been encoded"""
    BLOCKS_4 = (1 << 3)
    BLOCKS_8 = (1 << 2)
    BLOCKS_12 = (1 << 1)
    BLOCKS_16 = 1
    ALL = 0xF


class SBCChannelMode:
    """Indicate with which channel mode the frame has been
    encoded. The number of channels depends on this information."""
    CHANNEL_MODE_MONO = (1 << 3)
    CHANNEL_MODE_DUAL = (1 << 2)
    CHANNEL_MODE_STEREO = (1 << 1)
    CHANNEL_MODE_JOINT_STEREO = 1
    ALL = 0xF


class SBCAllocationMethod:
    """Indicates how the bit pool is allocated to different
    subbands. Either it is based on the loudness of the sub
    band signal or on the signal to noise ratio."""
    SNR = (1 << 1)
    LOUDNESS = 1
    ALL = 0x3


class SBCSubbands:
    """indicates the number of subbands with which the frame
    has been encoded"""
    SUBBANDS_4 = (1 << 1)
    SUBBANDS_8 = 1
    ALL = 0x3
