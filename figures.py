from re import U
import numpy as np
from numpy import arctan2, arccos, pi
import MyMath as mm
WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texCoords = texCoords
        self.sceneObj = sceneObj
        

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0, texture = None,  matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType


class Sphere(object):


    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = mm.resta_vector(self.center, orig)
        tca = mm.producto_punto(L, dir)
        d = (mm.norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # P = O + t0 * D
        #P = np.add(orig, t0 * np.array(dir))
        P = mm.suma_vector(orig, t0 * np.array(dir))
        normal = mm.resta_vector(P, self.center)
        normal = normal / mm.norm(normal)

        u = 1 *- (np.arctan2(normal[2], normal[0]) / (2 * np.pi) + 0.5)
        v = np.arccos(-normal[1]) / np.pi

        uvs = (u,v)


        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         texCoords= uvs,
                         sceneObj = self)

class Plane(object):

    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normal / np.linalg.norm(normal)
        #self.normal = normal / mm.dividir(normal, mm.norm(normal))
        self.material = material

    def ray_intersect(self, orig, dir):
        denom = mm.producto_punto(dir, self.normal)

        if abs(denom) > 0.0001:
            num = mm.producto_punto(mm.resta_vector(self.position ,orig), self.normal)
            t = num / denom
            if t > 0:
                P = mm.suma_vector(orig, t * np.array(dir))

                return Intersect(distance = t,
                                 point = P,
                                 normal = self.normal,
                                 texCoords = None,
                                 sceneObj = self)

        return None

class AABB(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material

        self.planes = []

        halfSizes = [0,0,0]

        halfSizes[0] = size[0] / 2
        halfSizes[1] = size[1] / 2
        halfSizes[2] = size[2] / 2

        self.planes.append(Plane(mm.suma_vector(position, (halfSizes[0], 0, 0)), (1, 0, 0), material))
        self.planes.append(Plane(mm.suma_vector(position, (-halfSizes[0], 0, 0)), (-1, 0, 0), material))

        self.planes.append(Plane(mm.suma_vector(position, (0,halfSizes[1], 0)), (0, 1, 0), material))
        self.planes.append(Plane(mm.suma_vector(position, (0,-halfSizes[1], 0)), (0,-1, 0), material))

        self.planes.append(Plane(mm.suma_vector(position, (0,0,halfSizes[2])), (0,0,1), material))
        self.planes.append(Plane(mm.suma_vector(position, (0,0,-halfSizes[2])), (0,0,-1), material))

        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + halfSizes[i])
            self.boundsMax[i] = self.position[i] + (epsilon + halfSizes[i])
    
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)

            
            if planeInter is not None:
                planePoint = planeInter.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter


        if intersect is None:
            return None
        
        return Intersect(distance = t,
                         point = intersect.point,
                         normal = intersect.normal,
                         texCoords= None,
                         sceneObj = self)

class Disk(object):
    def __init__(self, position, radius, normal,  material):
        self.plane = Plane(position, normal, material)
        self.material = material
        self.radius = radius

    def ray_intersect(self, orig, dir):

        intersect = self.plane.ray_intersect(orig, dir)

        if intersect is None:
            return None

        contact = mm.resta_vector(intersect.point, self.plane.position)
        contact = mm.norm(contact)

        if contact > self.radius:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = self.plane.normal,
                         texcoords = None,
                         sceneObj = self)

class Triangle(object):
    def __init__(self, v0, v1, v2, material):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = material

    def ray_intersect(self, orig, dir):
        edge1 = np.subtract(self.v1, self.v0)
        edge2 = np.subtract(self.v2, self.v0)

        h = np.cross(dir, edge2)
        a = np.dot(edge1, h)

        if a > -0.00001 and a < 0.00001:
            return None

        f = 1.0 / a
        s = np.subtract(orig, self.v0)
        u = f * np.dot(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = np.cross(s, edge1)
        v = f * np.dot(dir, q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * np.dot(edge2, q)

        if t > 0.00001:
            P = np.add(orig, t * np.array(dir))

            return Intersect(distance = t,
                             point = P,
                             normal = np.cross(edge1, edge2),
                             texCoords = None,
                             sceneObj = self)

        return None
                    

