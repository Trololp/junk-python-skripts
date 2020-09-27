#######################################
# an example using python to make some graphics.
# there i expirementing with lighting ray passes in concave sphere.
#######################################


from PilLite import Image
import math

size_h = 100
size_w = 100

π = math.pi

im = Image.new(size_w,size_h+255,'RGB', 0)


#sphere light from above
for X in range(size_w):
    for Y in range(size_h):
        x = (2*X/size_w - 1.0)
        y = (Y/size_h)
        if x*x + y*y < 1.0:
            z = math.sqrt(1-x*x-y*y)
            w = math.sqrt(z*z+x*x)
            color = math.sqrt(2*w*math.sqrt(1-w*w)*math.sqrt(1-x*x))/3
            color_int = int(255 * math.fabs(color))
            im.put_pixel((X, Y), 0x010000 * color_int + 0x0100 * color_int + color_int)

for Y in range(size_h):
    for X in range(size_w):
        x = (2*  X / size_w - 1.0)
        y = (2 * Y / size_h - 1.0)
        if x*x + y*y < 1.0:
            z = math.sqrt(1-x*x-y*y)
            w = math.sqrt(1-z*z)
            if w < 0.5:
                color = (1-2*w*w)/4
            else:
                beta = 2*math.asin(w)
                n = 2*π/(π-beta)
                N = math.ceil(n/2)
                n_round = math.floor(n)
                if n_round % 2:
                    delta_beta = ((π-2*π/n_round) - beta)*N + (π/2-beta/2)
                else:
                    delta_beta = ((π-2*π/n_round) - beta)*N
                color = math.cos(delta_beta)/4
            #color = math.sqrt(color)
            color_int = int(255 * math.fabs(color))

            im.put_pixel((X, Y), 0x010000 * color_int + 0x0100 * color_int + color_int)
            if Y == int(size_h/2):
                im.put_pixel((X, size_h + color_int), 0xFFFFFF00)

im.save('simplePixel.png') # or any image format

"""
MIT License
Copyright (c) 2017 Cyrille Rossant
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""