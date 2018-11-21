from enum import IntEnum
from struct import pack, unpack, calcsize
from io import SEEK_CUR, SEEK_SET, SEEK_END
from hashlib import md5, sha1, sha256, sha512
from binascii import hexlify as _hexlify, unhexlify
from ctypes import Structure, BigEndianStructure, sizeof

MD5_DIGEST_LEN = 16
SHA1_DIGEST_LEN = 20
SHA256_DIGEST_LEN = 32
SHA512_DIGEST_LEN = 64

def hexlify(b: (bytes, bytearray)) -> str:
    return _hexlify(b).decode("utf8")

class Endian(IntEnum):
    LITTLE = 0
    BIG = 1
    NETWORK = 2
    NATIVE = 3

class StreamIO(object):
    stream = None
    endian = None

    #I/O functions
    read_func = None
    write_func = None

    #attributes
    can_seek = False
    can_tell = False

    def __init__(self, stream, endian: Endian = Endian.LITTLE):
        self.set_stream(stream)
        self.set_endian(endian)
        self.set_io_funcs()

    #shortcuts
    def __len__(self) -> int:
        return self.length()

    def __bytes__(self) -> bytes:
        return self.getvalue()

    #utilities
    def set_stream(self, stream) -> None:
        """
        Set stream to read/write from/to
        :param stream: The stream to interact with
        :return: None
        """
        self.stream = stream
        self.can_seek = stream.seekable()
        self.can_tell = stream.seekable()

    def set_endian(self, endian: Endian) -> None:
        """
        Set the endian you want to use for reading/writing data in the stream
        :param endian: LITTLE, BIG, NETWORK, or NATIVE
        :return: None
        """
        endian = int(endian)
        endians = ["<", ">", "!", "@"]
        if endian in range(len(endians)):
            self.endian = endians[endian]

    def set_read_func(self, name: str) -> None:  #, *param_types):
        """
        Set the function name in the stream of the read function
        :param name: The name of the read function
        :return: None
        """
        if hasattr(self.stream, name):
            self.read_func = getattr(self.stream, name)

    def set_write_func(self, name: str) -> None:  #, *param_types):
        """
        Set the function name in the stream of the write function
        :param name: The name of the write function
        :return: None
        """
        if hasattr(self.stream, name):
            self.write_func = getattr(self.stream, name)

    def set_io_funcs(self, read_name: str = "read", write_name: str = "write") -> None:
        """
        Set the read/write function names in the stream
        :param read_name: The name of the read function
        :param write_name: The name of the write function
        :return: None
        """
        self.set_read_func(read_name)
        self.set_write_func(write_name)

    def tell(self) -> int:
        """
        Tell the current position of the stream if supported
        :return: The position of the stream
        """
        if self.can_tell:
            return self.stream.tell()
        raise NotImplementedError("tell isn't implemented in the specified stream!")

    def seek(self, index: int, whence: int = SEEK_SET) -> int:
        """
        Jump to a position in the stream if supported
        :param index: The offset to jump to
        :param whence: Index is interpreted relative to the position indicated by whence (SEEK_SET, SEEK_CUR, and SEEK_END in io library)
        :return: The new absolute position
        """
        if self.can_seek:
            return self.stream.seek(index, whence)
        raise NotImplementedError("seek isn't implemented in the specified stream!")

    def seek_start(self) -> int:
        """
        Jump to the beginning of the stream if supported
        :return: The new absolute position
        """
        return self.stream.seek(0)

    def seek_end(self) -> int:
        """
        Jump to the end of the stream if supported
        :return: The new absolute position
        """
        return self.stream.seek(0, SEEK_END)

    def length(self) -> int:
        """
        Get the length of the stream if supported
        :return: The total length of the stream
        """
        prev_loc = self.tell()
        self.seek_end()
        stream_len = self.tell()
        self.seek(prev_loc)
        return stream_len

    def getvalue(self) -> (bytes, bytearray):
        """
        Get the stream's output
        :return: The stream's data as bytes or bytearray
        """
        return self.stream.getvalue()

    def getbuffer(self) -> (bytes, bytearray):
        """
        Get the stream's buffer
        :return: The stream's buffer as bytes or bytearray
        """
        return self.stream.getbuffer()

    def flush(self) -> None:
        """
        Write the data to the stream
        :return: None
        """
        return self.stream.flush()

    def close(self) -> None:
        """
        Close the stream
        :return: None
        """
        self.stream.close()

    #base I/O methods
    def read(self, num: int = -1) -> (bytes, bytearray):
        if num <= 0:
            return self.read_func()
        return self.read_func(num)

    def write(self, data: (bytes, bytearray, int)) -> int:
        if isinstance(data, int):
            data = bytes([data])
        return self.write_func(data)

    def stream_unpack(self, fmt: str) -> (tuple, list):
        fmt = self.endian + fmt
        return unpack(fmt, self.read(calcsize(fmt)))

    def stream_pack(self, fmt: str, *values) -> int:
        fmt = self.endian + fmt
        return self.write(pack(fmt, *values))

    #bytes
    def read_sbyte(self) -> int:
        return self.stream_unpack("b")[0]

    def read_sbytes(self, num: int) -> (tuple, list):
        return self.stream_unpack(str(num) + "b")

    def write_sbyte(self, value: int) -> int:
        return self.stream_pack("b", value)

    def write_sbytes(self, values: (bytes, bytearray)) -> int:
        return self.stream_pack(str(len(values)) + "b", *values)

    #ubytes
    def read_byte(self) -> int:
        return self.stream_unpack("B")[0]

    def read_bytes(self, num: int) -> (bytes, bytearray):
        return bytes(self.stream_unpack(str(num) + "B"))

    def write_byte(self, value: int):
        return self.stream_pack("B", value)

    def write_bytes(self, values: (bytes, bytearray)) -> int:
        return self.stream_pack(str(len(values)) + "B", values)

    def load_from_buffer(self, data: (bytes, bytearray)) -> int:
        return self.write_bytes(data)

    #boolean
    def read_bool(self) -> bool:
        return self.stream_unpack("?")[0]

    def write_bool(self, value: bool) -> int:
        return self.stream_pack("?", value)

    #int16/short
    def read_int16(self) -> int:
        return self.stream_unpack("h")[0]

    def read_short(self) -> int:
        return self.read_int16()

    def write_int16(self, value: int) -> int:
        return self.stream_pack("h", value)

    def write_short(self, value: int) -> int:
        return self.write_int16(value)

    #uint16/ushort
    def read_uint16(self) -> int:
        return self.stream_unpack("H")[0]

    def read_ushort(self) -> int:
        return self.read_uint16()

    def write_uint16(self, value: int) -> int:
        return self.stream_pack("H", value)

    def write_ushort(self, value: int) -> int:
        return self.write_uint16(value)

    #int32/int/long
    def read_int32(self) -> int:
        return self.stream_unpack("i")[0]

    def read_int(self) -> int:
        return self.read_int32()

    def read_long(self) -> int:
        return self.read_int32()

    def write_int32(self, value: int) -> int:
        return self.stream_pack("i", value)

    def write_int(self, value: int) -> int:
        return self.write_int32(value)

    def write_long(self, value: int) -> int:
        return self.write_int32(value)

    #uint32/uint/ulong
    def read_uint32(self) -> int:
        return self.stream_unpack("I")[0]

    def read_uint(self) -> int:
        return self.read_uint32()

    def read_ulong(self) -> int:
        return self.read_uint32()

    def write_uint32(self, value: int) -> int:
        return self.stream_pack("I", value)

    def write_uint(self, value: int) -> int:
        return self.write_uint32(value)

    def write_ulong(self, value: int) -> int:
        return self.write_int32(value)

    #int64/longlong
    def read_int64(self) -> int:
        return self.stream_unpack("q")[0]

    def read_longlong(self) -> int:
        return self.read_int64()

    def write_int64(self, value: int) -> int:
        return self.stream_pack("q", value)

    def write_longlong(self, value: int) -> int:
        return self.write_int64(value)

    #uint64/ulonglong
    def read_uint64(self) -> int:
        return self.stream_unpack("Q")[0]

    def read_ulonglong(self) -> int:
        return self.read_uint64()

    def write_uint64(self, value: int) -> int:
        return self.stream_pack("Q", value)

    def write_ulonglong(self, value: int) -> int:
        return self.write_uint64(value)

    #float32/single
    def read_float32(self) -> float:
        return self.stream_unpack("f")[0]

    def read_single(self) -> float:
        return self.read_float32()

    def write_float32(self, value: float) -> float:
        return self.stream_pack("f", value)

    def write_single(self, value: float) -> float:
        return self.write_float32(value)

    #float64/double
    def read_float64(self) -> float:
        return self.stream_unpack("d")[0]

    def read_double(self) -> float:
        return self.read_float64()

    def write_float64(self, value: float) -> float:
        return self.stream_pack("d", value)

    def write_double(self, value: float) -> float:
        return self.write_float64(value)

    #varint
    def read_varint(self) -> int:
        shift = 0
        result = 0
        while True:
            i = self.read_byte()
            result |= (i & 0x7f) << shift
            shift += 7
            if not (i & 0x80):
                break
        return result

    def write_varint(self, num: int) -> int:
        buff = b""
        while True:
            towrite = num & 0x7f
            num >>= 7
            if num:
                buff += bytes([(towrite | 0x80)])
            else:
                buff += bytes([towrite])
                break
        return self.write_bytes(buff)

    #strings
    def read_7bit_encoded_int(self) -> int:
        index = 0
        result = 0
        while True:
            byte_value = self.read_byte()
            result |= (byte_value & 0x7F) << (7 * index)
            if byte_value & 0x80 == 0:
                break
            index += 1
        return result

    def write_7bit_encoded_int(self, value: int) -> int:
        data = b""
        num = value
        while num >= 0x80:
            data += bytes([((num | 0x80) & 0xFF)])
            num >>= 7
        data += bytes([num & 0xFF])
        return self.write(data)

    def read_string(self, encoding: str = "utf8") -> str:
        return self.read(self.read_7bit_encoded_int()).decode(encoding)

    def read_str(self, encoding: str = "utf8") -> str:
        return self.read_string(encoding)

    def write_string(self, value: str, encoding: str = "utf8") -> int:
        self.write_7bit_encoded_int(len(value))
        return self.write(value.encode(encoding))

    def write_str(self, value: str, encoding: str = "utf8") -> int:
        return self.write_string(value, encoding)

    #hex
    def read_hex(self, num: int) -> (bytes, bytearray):
        return hexlify(self.read(num))

    def write_hex(self, value: str) -> int:
        return self.write(unhexlify(value))

    #hashing
    def read_md5(self) -> (bytes, bytearray):
        return self.read(MD5_DIGEST_LEN)

    def read_sha1(self) -> (bytes, bytearray):
        return self.read(SHA1_DIGEST_LEN)

    def read_sha256(self) -> (bytes, bytearray):
        return self.read(SHA256_DIGEST_LEN)

    def read_sha512(self) -> (bytes, bytearray):
        return self.read(SHA512_DIGEST_LEN)

    def write_md5(self, data: (bytes, bytearray)) -> (bytes, bytearray):
        data_hash = md5(data).digest()
        self.write(data_hash)
        return data_hash

    def write_sha1(self, data: (bytes, bytearray)) -> (bytes, bytearray):
        data_hash = sha1(data).digest()
        self.write(data_hash)
        return data_hash

    def write_sha256(self, data: (bytes, bytearray)) -> (bytes, bytearray):
        data_hash = sha256(data).digest()
        self.write(data_hash)
        return data_hash

    def write_sha512(self, data: (bytes, bytearray)) -> (bytes, bytearray):
        data_hash = sha512(data).digest()
        self.write(data_hash)
        return data_hash

    #structures/structs
    def read_struct(self, struct_type: (Structure, BigEndianStructure)) -> (Structure, BigEndianStructure):
        return struct_type.from_buffer_copy(self.read(sizeof(struct_type)))

    def write_struct(self, struct_obj: (Structure, BigEndianStructure)) -> int:
        return self.write(bytes(struct_obj))