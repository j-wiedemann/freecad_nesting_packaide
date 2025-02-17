# freecad_nesting_packaide
Macros to Nest object with packaide python library

## Install Packaide (2D nesting python library)

```
git clone https://github.com/DanielLiamAnderson/Packaide.git
cd Packaide
git checkout v2
sudo apt install libcgal-dev
pip3 install --user . -r -requirements.txt
```

## USAGE

Modify lines 22 and 23 to set the sheet dimensions.

Select 2D objects to nest and run the macro "nesting_with_packaide.py"

![result](https://github.com/j-wiedemann/freecad_nesting_packaide/blob/main/Capture%20d%E2%80%99%C3%A9cran%20du%202025-02-17%2022-45-39.png)

## Notes
The importSVGCustom is needed to reimported nested parts and I only modify line 1619 :

```
--- for transformation, arguments in transformre.findall(tr):
+++ for transformation, arguments in reversed(transformre.findall(tr)):
```

