import Image,ImageOps
import gtk
import string
import StringIO

# from the FAQ

def pixbuf_to_pil (pb):
    assert(pb.get_colorspace() == gtk.gdk.COLORSPACE_RGB)
    dimensions = pb.get_width(), pb.get_height()
    stride = pb.get_rowstride()
    pixels = pb.get_pixels()
    mode = pb.get_has_alpha() and "RGBA" or "RGB"
    return Image.frombuffer(mode, dimensions, pixels,
                            "raw", mode, stride, 1)


# from http://www.daa.com.au/pipermail/pygtk/2003-June/005268.html
# (Sebastian Wilhelmi)

def pil_to_pixbuf (image):
    file = StringIO.StringIO()
    image.save(file, 'ppm')
    contents = file.getvalue()
    file.close()
    loader = gtk.gdk.PixbufLoader('pnm')
    loader.write (contents, len(contents))
    pixbuf = loader.get_pixbuf()
    loader.close()
    return pixbuf


def html_to_tuple (hexstr):
    # hackishly except 3 chars rather than 6
    if hexstr[0]=="#": hexstr=hexstr[1:]
    if len(hexstr)==3:
        hexstr = hexstr[0]+hexstr[0]+hexstr[1]+hexstr[1]+hexstr[2]+hexstr[2]
    if len(hexstr)!=6: raise ValueError('String must have 3 or 6 digits!')
    r = string.atoi(hexstr[0:2],16)
    g = string.atoi(hexstr[2:4],16)
    b = string.atoi(hexstr[4:],16)
    return (r,g,b)
        

def pixbuf_transform_color (pb,
                            initial_color,
                            target_color):
    """Return a pixbuf with one color transformed."""
    if type(initial_color)==str: initial_color=html_to_tuple(initial_color)
    if type(target_color)==str: target_color=html_to_tuple(target_color)
    arr = pb.get_pixels_array()
    arr = arr.copy()
    for row in arr:
        for pxl in row:
            if pxl[3]!=0: # not transparent
                if not initial_color or (pxl[0]==initial_color[0] and
                                         pxl[1]==initial_color[1] and
                                         pxl[2]==initial_color[2]):
                    pxl[0]=target_color[0]
                    pxl[1]=target_color[1]
                    pxl[2]=target_color[2]
    return gtk.gdk.pixbuf_new_from_array(arr,
                                         pb.get_colorspace(),
                                         pb.get_bits_per_sample()
                                         )

def colorize_pixbuf (pixbuf, black, white):
    i = pixbuf_to_pil(pixbuf)
    i.save('/tmp/test_pb.png','png')
    irgb = Image.open('/tmp/test_pb.png')
    irgb.save('/tmp/test_rgb.png','png')
    ig = irgb.convert('L')
    ig.save('/tmp/test_L.png','png')
    icol = ImageOps.colorize(ig,black,white)
    icol.save('/tmp/test.png','png')
    return pil_to_pixbuf(icol)
    #return pil_to_pixbuf(pixbuf_to_pil(pixbuf))
