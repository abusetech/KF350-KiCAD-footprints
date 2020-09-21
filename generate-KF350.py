import os.path

for POSITIONS in range(2,21):
    PITCH = 3.5
    MODNAME = "TerminalBlock_KF-KF350_1x{:01d}_P{:,.1f}".format(POSITIONS, PITCH)
    FILENAME = "TerminalBlock_KF-KF350_1x{:01d}_P{}".format(POSITIONS, str(PITCH).replace(".","-")) + ".kicad_mod"
    DESCRIPTION = "KF350 Terminal block."
    TAGS = "KF350"
    FAB_CLEAR = 0.5
    TEMPLATE = '''
    (module {modname}
        (descr "{desc}")
        (tags "{tags}")
        (fp_text reference REF** (at {ref_location}) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
    {drawing})
    '''

    def line(x1,y1,x2,y2, layer="F.SilkS", width=0.12):
        return "    (fp_line (start {} {}) (end {} {}) (layer {}) (width {}))\n".format(x1,y1,x2,y2,layer,width)

    def pad(n, x, y, size=2.4, drill=1.2, shape=None, layers="*.Cu *.Mask"):
        if shape == None:
            if n == 1:
                shape = "rect"
            else:
                shape = "circle"
        return "    (pad {} thru_hole {} (at {} {}) (size {} {}) (drill {}) (layers {}))\n".format(n, shape, x, y, size, size, drill, layers)

    #Front is in -Y
    drawing = ""
    #Bounding rectangle fab
    drawing += line(-2.0-FAB_CLEAR , 6.8-3.5+FAB_CLEAR , -2-FAB_CLEAR , -3.5-FAB_CLEAR , layer="F.Fab", width=0.1) #Vertical Left
    drawing += line((POSITIONS-1)*3.5+2.0+FAB_CLEAR , 6.8-3.5+FAB_CLEAR , (POSITIONS-1)*3.5+2+FAB_CLEAR , -3.5-FAB_CLEAR, layer="F.Fab", width=0.1) #Vertical Right
    drawing += line(-2.0-FAB_CLEAR , -3.5-FAB_CLEAR, (POSITIONS-1)*3.5+2+FAB_CLEAR, -3.5-FAB_CLEAR , layer="F.Fab", width=0.1) #Horizontal Front
    drawing += line((POSITIONS-1)*3.5+2.0+FAB_CLEAR, 6.8-3.5+FAB_CLEAR, -2-FAB_CLEAR, 6.8-3.5+FAB_CLEAR, layer="F.Fab", width=0.1) #Horizontal Back
    #Bounding rectangle silkscreen
    drawing += line(-2.0, 6.8-3.5, -2, -3.5) #Vertical Left
    drawing += line((POSITIONS-1)*3.5+2.0, 6.8-3.5, (POSITIONS-1)*3.5+2, -3.5) #Vertical Right
    drawing += line(-2.0, -3.5, (POSITIONS-1)*3.5+2, -3.5) #Horizontal Front
    drawing += line((POSITIONS-1)*3.5+2.0, 6.8-3.5, -2, 6.8-3.5) #Horizontal Back
    #Front corner marker
    drawing += line( -2-0.25, 3.3+0.25, -2-0.25, 2.3+0.25)
    drawing += line( -2-0.25, 3.3+0.25, -1.5+0.25
                     , 3.3+0.25)
    #Front Face Line
    drawing += line(-2.0, 3.3-1, (POSITIONS-1)*3.5+2, 3.3-1)
    #Pads
    for n in range(1,POSITIONS+1):
        drawing += pad(n, (n-1) * PITCH, 0)

    output = TEMPLATE.format(modname=MODNAME,
                    desc=DESCRIPTION,
                    tags = TAGS,
                    ref_location="{} 3.4".format(POSITIONS*3.5/2),
                    drawing=drawing
                    )
    print(FILENAME)
    with open(os.path.join("KF350.pretty", FILENAME), 'w') as f:
        f.write(output)
        f.flush()
