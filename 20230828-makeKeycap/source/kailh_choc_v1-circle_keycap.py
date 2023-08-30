import cadquery as cq

# ------------------ #
# SETTINGS scale: mm #
# ------------------ #

keycap = {
    "DIA": 29,
    "height": 4.8,
    "fillet": 1,
}

# 3D printer settings
printer = {
    "DIA": 0.36,
    # 'layerThickness': 0.2
}

# export settings
fileName = "kailh_choc_v1-DIA{0}mm".format(keycap["DIA"])
outputDir = "/"

# -------- #
# MODELING #
# -------- #

# keytop

keycap.update(
    [
        ("radius", keycap["DIA"] / 2),
        ("thickness", printer["DIA"] * 3),
        ("top_thickness", printer["DIA"] * 2),
    ]
)

fill = (
    cq.Workplane("front")
    .circle(keycap["radius"])
    .extrude(keycap["height"])
    .faces("+Z")
    .edges()
    .fillet(keycap["fillet"])
)

infill = (
    cq.Workplane("front")
    .circle(keycap["radius"] - keycap["thickness"])
    .extrude(keycap["height"] - keycap["top_thickness"])
    .faces("+Z")
    .edges()
    .fillet(keycap["fillet"] / 2)
)

keytop = fill.cut(infill)

# keycap STEM

clearance = printer["DIA"]

stem_plate = (
    cq.Workplane("front")
    .circle(keycap["radius"] - keycap["thickness"] - clearance)
    .extrude(keycap["thickness"])
)

stems = stem_plate.pushPoints([(3, 0), (-3, 0)]).eachpoint(
    lambda loc: cq.Workplane().rect(1.28, 4).extrude(-3).val().located(loc)
)

stem_plate = stem_plate.union(stems)

# ------ #
# EXPORT #
# ------ #

cq.exporters.export(keytop, "{0}/{1}.stl".format(outputDir, fileName))
cq.exporters.export(stem_plate, "{0}/{1}_stem.stl".format(outputDir, fileName))
