# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 19:38:38 2023

@author: Quentin Barbier
"""

import re
import os
 
# set the directory path for the new folder
directory = "output"
 
# create the new directory
if not os.path.exists(directory):
    os.mkdir(directory)
 
# input file:
xml_file = 'Bergslagsparken.xml'
 
# open and read the contents of the xml file
with open(xml_file, 'r') as file:
    text = file.read()
    text = text.replace(".</P>", ".0</P>")
 
# split the text into different strings, one for every surface
text = text.split(sep='<Surface name=')
var_nr = 0
 
# for every surface create a mesh
for var in text[1:]:
    name = (var.split()[0]).replace("\"", "")
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
    
    # Write the mesh file
    with open(new_mesh_file, "w") as file:
        file.write("MESH2D\n")
        for point in points:
            file.write(point+"\n")
        for triangle in triangles:
            file.write(triangle+"\n")
    var_nr += 1
