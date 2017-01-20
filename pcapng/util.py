import struct
import sys
import time
import math


def is_python2():
    (major, minor, micro, release_level, serial) = sys.version_info
    return ((major == 2) and (minor == 7))

def is_python3():
    (major, minor, micro, release_level, serial) = sys.version_info
    return ((major == 3) and (minor >= 5))

def assert_python2():
    assert is_python2()

def assert_type_bytearray( arg ):
    assert type( arg ) == bytearray

def assert_type_bytes( arg ):
    assert type( arg ) == bytes

def assert_type_str( arg ):
    assert type( arg ) == str

def assert_type_list( arg ):
    assert type( arg ) == list

def assert_type_dict( arg ):
    assert type( arg ) == dict

def assert_uint8(arg):        # unsigned byte
    assert (0 <= arg <= 255)

def assert_int8(arg):          # signed byte
    assert (-128 <= arg <= 127)



def to_bytes( arg ):
    return bytes( bytearray( arg ))    # if python2, 'bytes' is synonym for 'str'

#todo move to pcap
def fmt_pcap_hdr( ts_sec, ts_usec, incl_len, orig_len ):
    packed = struct.pack( '>LLLL', ts_sec, ts_usec, incl_len, orig_len)
    return packed

def split_float( fval ):
    frac, whole = math.modf( fval )
    micros = int( round( frac * 1000000 ))
    return int(whole), micros

def curr_utc_time_tuple():
    utc_secs = time.time()
    secs, usecs = split_float( utc_secs )
    return secs, usecs

def timetup_to_float( secs, usecs ):
    return secs + (usecs / 1000000.0)

def timetup_subtract( ts1, ts2 ):
    (s1, us1) = ts1
    (s2, us2) = ts2
    t1 = timetup_to_float( s1, us1 )
    t2 = timetup_to_float( s2, us2 )
    delta = t2 - t1
    return delta

def ChrList_to_str(arg):
    #todo verify input type & values [0..255]
    strval = ''.join( arg )
    return strval

def first( lst ):
    return lst[0]

#todo move to pcapng.bytes
#-----------------------------------------------------------------------------

def block32_pad_len(curr_len):
    curr_blks = float(curr_len) / 4.0
    pad_blks = int( math.ceil( curr_blks ))
    pad_len = pad_blks * 4
    return pad_len

def pad_to_len(data, tolen, padval=0):
    elem_needed = tolen - len(data)
    assert (elem_needed >= 0), "padding cannot be negative"
    result = to_bytes(data) + to_bytes( [padval] )*elem_needed
    return result

def pad_to_block32(data):
    pad_len = block32_pad_len( len(data) )
    result = pad_to_len(data, pad_len)
    return result

def assert_block32_size(data):
    assert (0 == len(data) % 4), "data must be 32-bit aligned"
    return True

