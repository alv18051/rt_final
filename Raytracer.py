
from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 256
height = 256

# Materiales

snow = Material(diffuse = (0.6,0.6,0.6))
button = Material(diffuse = (0,0,0),spec = 8, matType= OPAQUE)
smile = Material(diffuse = (0.75,0.75,0.75),spec = 8, matType= OPAQUE)
eyes = Material(diffuse = (1,1,1),spec = 8, matType= OPAQUE)
nose = Material(diffuse = (0.93,0.56,0.13),spec = 8, matType= OPAQUE)

snow = Material(diffuse = (0.6, 0.6, 0.6), spec = 16, matType= OPAQUE)
wood = Material(diffuse = (0.5, 0.2, 0), spec = 8, matType= OPAQUE)
grass = Material(diffuse = (0, 0.5, 0), spec = 8, matType= OPAQUE)
marble = Material(diffuse = (0.95, 0.95, 0.95), spec = 8, matType= REFLECTIVE)

mirror = Material(diffuse = (0.9, 0, 0.9), spec = 64, matType = REFLECTIVE)
mirror2 = Material(diffuse = (0.5, 0.8, 0.9), spec = 64, matType = TRANSPARENT)
mirror3 = Material(diffuse = (0.5, 0.8, 0.9), spec = 64, matType = OPAQUE)

water = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 1.01, matType = OPAQUE)
yellowSubmarine = Material(diffuse = (0, 0.9, 0.9), spec = 64, ior = 2.45, matType = REFLECTIVE)
earth = Material(texture = Texture('handgun_Te.bmp'), matType = OPAQUE)

rtx = Raytracer(width, height)

rtx.envMap = Texture("map.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))

#rtx.scene.append( Sphere(V3(0, -1.4, -10), 0.5, earth) )
rtx.scene.append(Sphere(V3(-0.5,2.7,-10), 0.31, eyes))
rtx.scene.append(Sphere(V3(0.5,2.7,-10), 0.31, eyes))
rtx.scene.append(Sphere(V3(-0.45,2.4,-9), 0.19, button))
rtx.scene.append(Sphere(V3(0.45,2.4,-9), 0.19, button))

rtx.scene.append(Sphere(V3(0,0.9,-10), 0.24, button))
rtx.scene.append(Sphere(V3(0,-0.9,-10), 0.26, button))
rtx.scene.append(Sphere(V3(0,-2.9,-10), 0.4, button))

rtx.scene.append(Sphere(V3(0,3,-14), 2, snow))
rtx.scene.append(Sphere(V3(0,0,-14), 2.5, snow))
rtx.scene.append(Sphere(V3(0,-3,-14), 3, snow))

#rtx.scene.append(Sphere(V3(0,2.2,-10), 0.35, nose))

rtx.scene.append(Sphere(V3(0,1.4,-10), 0.15, smile))
rtx.scene.append(Sphere(V3(0.4,1.5,-10), 0.15, smile))
rtx.scene.append(Sphere(V3(-0.4,1.5,-10), 0.15, smile))
rtx.scene.append(Sphere(V3(0.7,1.6,-10), 0.15, smile))
rtx.scene.append(Sphere(V3(-0.7,1.6,-10), 0.15, smile))
rtx.scene.append(Plane(position= (0,-20,0), normal= (0,1,0), material= yellowSubmarine))
rtx.scene.append(AABB(position=(-2,-13,-10), size=(2,2,2), material= mirror))
rtx.scene.append(AABB(position=(2,-13,-10), size=(2,2,2), material= mirror))


rtx.scene.append(Triangle(V3(-1,2,-5), V3(0,3,-5), V3(1,2,-5), material= mirror))





rtx.glRender()

rtx.glFinish("output.bmp")