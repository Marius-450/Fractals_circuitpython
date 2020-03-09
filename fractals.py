# Fractals lib by Marius-450
import displayio

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

    # Definition des constantes


    # N = nombre d'iterations = nombre de couleurs
    # max : 256
    #N=100
    #N = 280


    #WIDTH=240
    #HEIGHT=240

    # Echelle



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

    # definition de l'objet bitmap

    bitmap = displayio.Bitmap(WIDTH, HEIGHT, N)

    # construction de la palette de N couleurs

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

    # On construit une grille contenant le bitmap

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)


    group.append(tile_grid)

    #############################

    # Dessin de Mandelbrot      #

    #############################

    def mandelbrot_core(x,y,iterations):
        c=x+y*1j
        z=c
        i=0
        while abs(z)<2 and i<iterations:
            i+=1
            z=z*z+c
        return -1 if i>=iterations else i



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