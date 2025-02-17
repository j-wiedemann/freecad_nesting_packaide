# Example usage of Packaide
import io
import xml.sax

import FreeCAD
import FreeCADGui

import Draft
import importSVGCustom

import packaide

# Install Packaide (2D nesting python library)

# git clone https://github.com/DanielLiamAnderson/Packaide.git
# cd Packaide
# git checkout v2
# sudo apt install libcgal-dev
# pip3 install --user . -r -requirements.txt

# Global VARIABLES
WIDTH = 150
HEIGHT = 100

svg_export_style = 0

print("""#########################
          # Nesting with Packaide #
          # #######################""")

# Code from importSVG
bb = FreeCAD.BoundBox()
for obj in FreeCADGui.Selection.getSelection():
    if (hasattr(obj, "Shape")
            and obj.Shape
            and obj.Shape.BoundBox.isValid()):
        bb.add(obj.Shape.BoundBox)

minx = bb.XMin
maxx = bb.XMax
miny = bb.YMin
maxy = bb.YMax

margin = 0

minx -= margin
maxx += margin
miny -= margin
maxy += margin
sizex = maxx - minx
sizey = maxy - miny
miny += margin

svg = '<svg'
svg += ' width="' + str(sizex) + '" height="' + str(sizey) + '"'
if svg_export_style == 0:
    svg += ' viewBox="0 0 ' + str(sizex) + ' ' + str(sizey) + '"'
else:
    svg += ' viewBox="%f %f %f %f"' % (minx, -maxy, sizex, sizey)
svg += ' xmlns="http://www.w3.org/2000/svg" version="1.1"'
svg += '>\n'

# Write paths
for ob in FreeCADGui.Selection.getSelection():
    if svg_export_style == 0:
        svg += '<g id="%s" transform="translate(%f,%f) '\
            'scale(1,-1)">\n' % (ob.Name, -minx, maxy)
    else:
        svg += '<g id="%s" transform="scale(1,-1)">\n' % ob.Name
    
    svg += Draft.get_svg(ob, override=False)
    _label_enc = str(ob.Label.encode('utf8'))
    _label = _label_enc.replace('<', '&lt;').replace('>', '&gt;')
    svg += '<title>%s</title>\n' % _label
    svg += '</g>\n'
svg += '</svg>'


# SVG definition of the sheet
sheet = f"""
<svg width="{WIDTH}mm" height="{HEIGHT}mm" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg"></svg>
""".format(WIDTH, HEIGHT)

# Attempts to pack as many of the parts as possible.
result, placed, fails = packaide.pack(
    [sheet]*100,                  # A list of sheets (SVG documents)
    svg,                   # An SVG document containing the parts
    tolerance = 0.5,          # Discretization tolerance
    offset = 0,               # The offset distance around each shape (dilation)
    partial_solution = True,  # Whether to return a partial solution
    rotations = 720,            # The number of rotations of parts to try
    persist = True            # Cache results to speed up next run
)

print("{} parts were placed on {} sheet(s). {} parts could not fit on the sheets".format(placed, len(result), fails))

for i, out in result:
    # Code from importSVG
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_external_ges, False)
    parser.setContentHandler(importSVGCustom.svgHandler())
    parser._cont_handler.doc = FreeCAD.ActiveDocument
    out_file_like = io.StringIO(out)
    parser.parse(out_file_like)
    FreeCAD.ActiveDocument.recompute()



