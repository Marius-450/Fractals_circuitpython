# Fractals lib by Marius-450
import displayio
import math
import random
import ulab
import gc
import time

mandelbrot_points = (((-0.5, 0), 2.3),
                     ((-.7435669, .1314023), .0022878),
                     ((-.7435669, .1314023), .022878),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 1),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.1),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.01),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.001),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.000878),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.000439),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.0002195),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.00010975),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.0001),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.000054875),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.000045),
                     ((-0.743643887037158704752191506114774, 0.131825904205311970493132056385139), 0.00002743),
                     ((-0.9534516777343751, -0.2587336923828125), 0.009902734375),
                     ((-0.235125, 0.827215), 0.00006))

def mandelbrot(WIDTH, HEIGHT, N=256, group=None, CENTER=(-0.5, 0), DIAMX=2.3):
    """
    mandelbrot()
    return a group with drawing of mandelbrot fractal in it.

    Parameters :
        WIDTH : width of the bitmap
        HEIGHT : height of the bitmap
        N : number of iterations, and number of colors (default 256)
        group : reuse a group instead of creating a new one
        CENTER : tuple containing the center coordinates
        DIAMX : "zoom" level, from 2.3 to 0.000027
    """

    DIAMY = DIAMX*HEIGHT/WIDTH

    XMIN=CENTER[0]-DIAMX/2
    XMAX=CENTER[0]+DIAMX/2

    YMIN=CENTER[1]-DIAMY/2
    YMAX=CENTER[1]+DIAMY/2

    dx=(XMAX-XMIN)/WIDTH
    dy=(YMAX-YMIN)/HEIGHT

    if group is None:
        group = displayio.Group()
    elif group:
        group.pop()

    bitmap = displayio.Bitmap(WIDTH, HEIGHT, N)

    def ColorMap(p):
        sr = sg = sb = 0
        if (p < 64):
            sr=0 ; sg=p*4 ; sb=255
        elif (p < 128):
            sr=(p-64)*4 ; sg=255 ; sb=(255-(p-64)*4)
        elif (p < 192):
            sr=255 ; sg=255  ;sb = (p-128)*4
        elif (p < 256):
            sr=255 ; sg=(255-(p-191)*4) ; sb= (255-(p-191)*4)
        return (sr,sg,sb)

    palette = displayio.Palette(N)

    for i in range(N):
        r=255*i//(N-1)
        s=ColorMap(r)
        palette[i]=s[0]*2**16+s[1]*2**8+s[2]

    palette[0]=0
    palette[1]=0xffffff

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group.append(tile_grid)

    #############################

    # Mandelbrot Drawing        #

    #############################
    def mandelbrot_core(creal,cimag,maxiter):
        real = creal
        imag = cimag
        for n in range(maxiter):
            real2 = real*real
            imag2 = imag*imag
            if real2 + imag2 > 4.0:
                return n
            imag = 2* real*imag + cimag
            real = real2 - imag2 + creal
        return -1

    x=XMIN
    print("Start drawing mandelbrot fractal :", CENTER, DIAMX, N)
    for xp in range(WIDTH):
        y=YMIN
        for yp in range(HEIGHT):
            bitmap[xp,yp]=mandelbrot_core(x,y,N-1)+1
            y += dy
        x += dx
        #display2.refresh_soon()

    return group


def mandelbrot_ulab(WIDTH, HEIGHT, N=256, group=None, CENTER=(-0.5, 0), DIAMX=2.3):
    """
    mandelbrot()
    return a group with drawing of mandelbrot fractal in it.

    Parameters :
        WIDTH : width of the bitmap
        HEIGHT : height of the bitmap
        N : number of iterations, and number of colors (default 256)
        group : reuse a group instead of creating a new one
        CENTER : tuple containing the center coordinates
        DIAMX : "zoom" level, from 2.3 to 0.000027
    """

    DIAMY = DIAMX*HEIGHT/WIDTH

    XMIN=CENTER[0]-DIAMX/2
    XMAX=CENTER[0]+DIAMX/2

    YMIN=CENTER[1]-DIAMY/2
    YMAX=CENTER[1]+DIAMY/2

    r1 = ulab.linspace(XMIN, XMAX, num=WIDTH)
    r2 = ulab.linspace(YMIN, YMAX, num=HEIGHT)
    if group is None:
        group = displayio.Group()
    elif group:
        group.pop()

    bitmap = displayio.Bitmap(WIDTH, HEIGHT, N)

    def ColorMap(p):
        sr = sg = sb = 0
        if (p < 64):
            sr=0 ; sg=p*4 ; sb=255
        elif (p < 128):
            sr=(p-64)*4 ; sg=255 ; sb=(255-(p-64)*4)
        elif (p < 192):
            sr=255 ; sg=255  ;sb = (p-128)*4
        elif (p < 256):
            sr=255 ; sg=(255-(p-191)*4) ; sb= (255-(p-191)*4)
        return (sr,sg,sb)

    palette = displayio.Palette(N)

    for i in range(N):
        r=255*i//(N-1)
        s=ColorMap(r)
        palette[i]=s[0]*2**16+s[1]*2**8+s[2]

    palette[0]=0
    palette[1]=0xffffff

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group.append(tile_grid)

    #############################

    # Mandelbrot Drawing        #

    #############################
    before = 0
    loop = 0
    after = 0

    print("Start drawing mandelbrot fractal :", CENTER, DIAMX, N)
    start = time.monotonic()
    for xp in range(WIDTH):
        s_before = time.monotonic()
        col_z_imag = ulab.array(r2)
        x = ulab.ones(HEIGHT)*r1[xp]
        x2 = x * x
        z2 = col_z_imag * col_z_imag
        output = ulab.zeros(HEIGHT, dtype=ulab.int16)
        notdone = [True]*HEIGHT
        before += time.monotonic() - s_before
        s_loop = time.monotonic()
        for i in range(N):
            z2 = col_z_imag * col_z_imag
            x2 = x * x
            try:
                output[(x2 + z2 ) < 4] = i
            except IndexError:
                break
            #col_z_imag[notdone] = ( ( x * col_z_imag )[notdone] * 2 ) + r2[notdone]
            col_z_imag = ( ( x * col_z_imag ) * 2 ) + r2
            #x[notdone] = (x2 - z2)[notdone] + r1[xp]
            x = (x2 - z2) + r1[xp]
        loop += time.monotonic() - s_loop
        s_after = time.monotonic()

        limit = output >= N-1
        if limit.count(True) > 0:
            output[limit] = -1
        output = output + 1
        for yp in range(HEIGHT):
            bitmap[xp,yp]= output[yp]
        after += time.monotonic() - s_after
    print("before :", before)
    print("loop   :", loop)
    print("after  :", after)
    print("total  :", time.monotonic() - start)
    return group







def quasicrystal(width, height, N=256, group=None, f=None, p=None, n=None):
    """
    # Quasicrystal Pattern Generator
    # https://code.activestate.com/recipes/579094-quasicrystal-pattern-generator/
    # https://en.wikipedia.org/wiki/Quasicrystal
    # http://mainisusuallyafunction.blogspot.com/2011/10/quasicrystals-as-sums-of-waves-in-plane.html
    #
    N : number of colors (default : 256)
    group : displayio.Group object.
    f : frequency, int [5-30] (default : random)
    p : phase, float [0-pi] (default : random)
    n : rotations, int [5-20] (default: random)
    (range indicate random range choice)
    """

    if group is None:
        group = displayio.Group()
    elif group:
        group.pop()
        gc.collect()
    pixels = displayio.Bitmap(width, height, N)
    palette = displayio.Palette(N)

    def ColorMap(p):
        sr = sg = sb = 0
        if (p < 64):
            sr=0 ; sg=p*4 ; sb=255
        elif (p < 128):
            sr=(p-64)*4 ; sg=255 ; sb=(255-(p-64)*4)
        elif (p < 192):
            sr=255 ; sg=255  ;sb = (p-128)*4
        elif (p < 256):
            sr=255 ; sg=(255-(p-191)*4) ; sb= (255-(p-191)*4)
        return (sr,sg,sb)

    for i in range(N):
        r=255*i//(N-1)
        s=ColorMap(r)
        palette[i]=s[0]*2**16+s[1]*2**8+s[2]

    # blue to yellow
    #for i in range(N):
    #    j = int((i/N)*255)
    #    palette[i]=j*2**16+j*2**8+128-j//2
    #palette[0] = 0x000088

    # grayscale
    #for i in range(N):
        #j = 128+int(i*(128/N))
    #    j = int((i/N)*255)
    #    palette[i]=j*2**16+j*2**8+j
    #palette[0] = 0

    tile_grid = displayio.TileGrid(pixels, pixel_shader=palette)
    group.append(tile_grid)
    if f is None:
        f = random.random() * 27 + 8 # frequency
    if p is None:
        p = random.random() * math.pi # phase
    if n is None:
        n = random.randint(7, 15) # of rotations
    # intermediary calculus
    fp = f + p
    rot = 3.14 * 2.0 / n
    Nn = (N - 1) / n
    h4pi = 12.56 / (height - 1)
    w4pi = 12.56 / (width - 1)
    row = ulab.array([i for i in range(width)])
    row = (row * w4pi) - 6.28
    for ky in range(height):
        y = ky * h4pi - 6.28
        y2 = y**2
        atan = ulab.vector.atan( row / y )
        dist = ulab.vector.sqrt((row * row) + y2) * fp
        #dist = dist * fp
        z = ulab.zeros(width)
        for i in range(n):
            z = z + ulab.vector.cos(ulab.vector.sin(atan + (i * rot)) * dist)
        z = abs(z * Nn)
        for i, c in enumerate(z):
            pixels[ky*width+i] = int(c)
        gc.collect()
    return group



def quasicrystal_opt(width, height, N=256, group=None, f=None, p=None, n=None):
    """
    # Quasicrystal Pattern Generator
    # https://code.activestate.com/recipes/579094-quasicrystal-pattern-generator/
    # https://en.wikipedia.org/wiki/Quasicrystal
    # http://mainisusuallyafunction.blogspot.com/2011/10/quasicrystals-as-sums-of-waves-in-plane.html
    #
    N : number of colors (default : 256)
    group : displayio.Group object.
    f : frequency, int [5-30] (default : random)
    p : phase, float [0-pi] (default : random)
    n : rotations, int [5-20] (default: random)
    (range indicate random range choice)
    """

    init = 0
    init_calc = 0
    time_row = 0
    inner = 0
    draw = 0

    start = time.monotonic()

    if group is None:
        group = displayio.Group()
    elif group:
        group.pop()
    gc.collect()
    pixels = displayio.Bitmap(width, height, N)
    palette = displayio.Palette(N)

    # corral colors
    def ColorMap(p):
        sr = sg = sb = 0
        if (p < 64):
            sr=0 ; sg=p*4 ; sb=255
        elif (p < 128):
            sr=(p-64)*4 ; sg=255 ; sb=(255-(p-64)*4)
        elif (p < 192):
            sr=255 ; sg=255  ;sb = (p-128)*4
        elif (p < 256):
            sr=255 ; sg=(255-(p-191)*4) ; sb= (255-(p-191)*4)
        return (sr,sg,sb)

    for i in range(N):
        r=255*i//(N-1)
        s=ColorMap(r)
        palette[i]=s[0]*2**16+s[1]*2**8+s[2]

    # blue to yellow
    #for i in range(N):
    #    j = int((i/N)*255)
    #    palette[i]=j*2**16+j*2**8+128-j//2
    #palette[0] = 0x000088

    # grayscale
    #for i in range(N):
        #j = 128+int(i*(128/N))
    #    j = int((i/N)*255)
    #    palette[i]=j*2**16+j*2**8+j
    #palette[0] = 0

    tile_grid = displayio.TileGrid(pixels, pixel_shader=palette)
    group.append(tile_grid)
    if f is None:
        f = random.random() * 27 + 8 # frequency
    if p is None:
        p = random.random() * math.pi # phase
    if n is None:
        n = random.randint(7, 15) # of rotations
    init += time.monotonic() - start
    # intermediary calculus
    start = time.monotonic()
    fp = f + p
    rot = 3.14 * 2.0 / n
    Nn = (N - 1) / n
    #row = ulab.array([i for i in range(width)])
    row = ulab.linspace(-6.28, 0, num=width//2)
    col = ulab.linspace(-6.28, 0, num=height//2)
    #x2 = row * row
    #y2 = col * col
    ky = 0
    init_calc += time.monotonic() - start
    for y in col:
        s_row = time.monotonic()
        #y = ky * h4pi - 6.28
        #y2 = y**2
        atan = ulab.vector.arctan2( col[ky], row )
        #atan = ulab.vector.atan( row / y )
        dist = ulab.vector.sqrt((row * row) + (y**2)) * fp
        #dist = dist * fp
        z = ulab.zeros(width//2)
        s_inner = time.monotonic()
        for i in range(n):
            z = z + ulab.vector.cos(ulab.vector.sin(atan + (i * rot)) * dist)
        inner += time.monotonic() - s_inner
        z = abs(z * Nn)
        time_row += time.monotonic() - s_row
        s_draw = time.monotonic()
        for i, c in enumerate(z):
            pixels[ky*width+i] = int(c)
            pixels[ky*width+(width-1 -i)] = int(c)
            pixels[(height-1-ky)*width+i] = int(c)
            pixels[(height-1-ky)*width+(width-1 -i)] = int(c)

        draw += time.monotonic() - s_draw
        ky += 1
        #gc.collect()
    #gc.collect()
    print("time report :")
    print(" init       :", init)
    print(" init calc  :", init_calc)
    print(" rows       :", time_row-inner)
    print("  inner loop:", inner)
    print(" draw       :", draw)

    return group
