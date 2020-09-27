import struct
import base64
f = open('data', 'rb')
f2 = open('data.txt', 'w')
f3 = open('data_base64undecoded', 'wb')
f4 = open('data_base64.txt', 'r')
magic_str = struct.unpack('8s', f.read(8))[0]
f.seek(16)

def write_to_decoded_file(str):
    bytestr = base64.b64decode(str)
    f3.write(bytestr)
    #f3.write(b'') #separator


while True:
    type = f.read(1)
    if type == b'':
        break
    if type == None:
        break
    if type == '':
        break


    if type < b'\x80':
        str = struct.unpack(f"{type[0]}s", f.read(type[0]))[0]
        f2.write(str.decode("utf-8") + '\n' )
    if type == b'\x80':
        extra_len = struct.unpack('i', f.read(4))[0]
        str = struct.unpack(f"{extra_len}s", f.read(extra_len))[0]
        f2.write(str.decode("utf-8") + '\n' )
    if type == b'\xFE':
        f2.write(f"int : {struct.unpack('i', f.read(4))[0]} \n")
    if type == b'\xFD':
        f2.write(f"float : {struct.unpack('f', f.read(4))[0]} \n")

for line in f4:
    write_to_decoded_file(line)



f.close()
f2.close()
f3.close()
f4.close()
