# -*- coding: utf-8 -*-
#LANDxml to mesh
intro = '''
Kretslopp och Vatten - 2023
This script converts a LANDxml file into .2dm mesh file
The mesh file(s) are saved in a new folder at the same location as the xml file
A separate mesh will be created for every surface within the xml file
This script might not work with every LANDxml format.
'''
print(intro)
import re
import os
from tkinter import Tk, filedialog

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
print("Välj LANDxml fil")
xml_file = str(filedialog.askopenfilename()) # retrieve the folder directory

file_name = os.path.basename(xml_file)
directory= f'{os.path.dirname(xml_file)}/{file_name}_mesh'
from pathlib import Path
Path('/root/dir/sub/file.ext').stem
#create the new directory
if not os.path.exists(directory):
    os.mkdir(directory)

# open and read the contents of the xml file
with open(xml_file, 'r') as file:
    text = file.read()
    text = text.replace(".</P>", ".0</P>")
    text = text.replace(". ", ".0 ")
# split the text into different strings, one for every surface
text = text.split(sep='<Surface name=')
var_nr = 0
# for every surface create a mesh
for var in text[1:]:
    # extract the surface name 
    name = (var.split('"')[1])
    # Use the surface name to title the mesh file
    new_mesh_file = f'{directory}/mesh_{name}.2dm'
    
# extracting the points
    pattern = r'<P id="(\d+)">(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)</P>'
    matches = re.findall(pattern, var)
    
    # append the triangles list
    points = []
    for m in matches:
        id, y, x, z = m
        points.append(f'ND {id} {x} {y} {z}')
    
    # same thing for triangles
    pattern2 = r'<F n="(\d+)\s+(\d+)\s+(\d+)">(\d+)\s+(\d+)\s+(\d+)</F>'
    matches2 = re.findall(pattern2, var)
    n=1
    triangles = []
    for m in matches2:
        a, b, c, d, e, f = m
        triangles.append(f'E3T {n} {d} {e} {f}')
        n += 1
        
    # extra pattern that is sometimes used in xml triangle definition 
    pattern3 = r'<F>(\d+)\s+(\d+)\s+(\d+)</F>'
    matches3 = re.findall(pattern3, var)
    
    n=1
    for m in matches3:
        d, e, f = m
        triangles.append(f'E3T {n} {d} {e} {f}')
        n += 1
    
    # Write the mesh file
    with open(new_mesh_file, "w") as file:
        file.write("MESH2D\n")
        for point in points:
            file.write(point+"\n")
        for triangle in triangles:
            file.write(triangle+"\n")
    var_nr += 1
