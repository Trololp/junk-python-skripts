from os import listdir
from os.path import isfile, join
from struct import *

mypath = 'E:\\ВАНЯ\\HLMV\\bspviewer\\bspv new version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\\Half-Life Maps'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


leaf_contents = {
    -1:  'CONTENTS_EMPTY',
    -2:  'CONTENTS_SOLID',
    -3:  'CONTENTS_WATER',
    -4:  'CONTENTS_SLIME',
    -5:  'CONTENTS_LAVA',
    -6:  'CONTENTS_SKY',
    -7:  'CONTENTS_ORIGIN',
    -8:  'CONTENTS_CLIP',
    -9:  'CONTENTS_CURRENT_0',
    -10: 'CONTENTS_CURRENT_90',
    -11: 'CONTENTS_CURRENT_180',
    -12: 'CONTENTS_CURRENT_270',
    -13: 'CONTENTS_CURRENT_UP',
    -14: 'CONTENTS_CURRENT_DOWN',
    -15: 'CONTENTS_TRANSLUCENT'

}


def read_bsp(bsp_file):
    version = bsp_file.read(4)
    if(version != b'\x1E\x00\x00\x00'):
        print('no hl_map file !')
        return

    lumps = []
    lumps_f = bsp_file.read(13*8)

    for i in range(0, 13):
        lumps.append(unpack('ii', lumps_f[0+i*8:8+i*8]))


    (offset, size) = lumps[10]
    leaves_count = size//28
    print(leaves_count)

    bsp_file.seek(offset)

    for j in range(0, leaves_count):
        leave = bsp_file.read(28)
        (nContent, nVisOffset, nMinsx, nMinsy, nMinsz, nMaxsx, nMaxsy, nMaxsz, iFirstMarkSurface, nMarkSurfaces,
         al1, al2, al3, al4,) = unpack('iihhhhhhhhBBBB',leave)

        if(nContent >= -2 or nContent == -6 or nContent == -3):
            continue

        print(f'nContent = {nContent}({leaf_contents[nContent]}), nVisOffset = {nVisOffset}, nMins = [{nMinsx} {nMinsy} {nMinsz}], nMaxs = [{nMaxsx} {nMaxsy} {nMaxsz}],'
              f' iFirstMarkSurface = {iFirstMarkSurface}, nMarkSurfaces = {nMarkSurfaces}, '
              f'Ambientlevels = [{al1}, {al2}, {al3}, {al4}]')


s = 0

for file_name in onlyfiles:
    bsp_file = open(f'{mypath}\\{file_name}', 'rb')
    print(file_name)
    read_bsp(bsp_file)
    bsp_file.close()
    s+=1

