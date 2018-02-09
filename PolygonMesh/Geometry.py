"""
.. module:: Geometry
    :platform: Unix, Windows Linux
    :synopsis: Modul which geometric Functions

.. module:: Martin Denk <denkmartin@web.de>


"""

import numpy as np

class Point(object):
    """ Point with attributes

    :param id(int): Point ID
    :param x(float): x-Coordinate
    :param y(float): y-Coordinate
    :param z(float): z-Coordinate


    Example for creating a tirangle object

    >>> p1 = Point(1, 1.0, 1.0, 1.0)
    """

    def __init__(self,ID=None, X=None, Y=None, Z=None, ):
        self.__x = X
        self.__y = Y
        self.__z = Z
        self.__id = ID


    @property
    def id(self):
        return self.__id

    @ id.setter
    def id(self, ID):
        self.__id = ID

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, z):
        self.__z = z

class Triangle(object):
    """ Triangle which is defined by 3 points

    :param id(int): Triangle ID
    :param points(list(Point)): 3 Points for the triangle
    :param normal(list(float)): Normal-Vector of plane


    Example for creating a tirangle object

    >>> p1 = Point(1, 1.0, 1.0, 1.0)
    >>> p2 = Point(2, 2.0, 2.0, 2.0)
    >>> p3 = Point(3, 1.0, 2.0, 0.0)
    >>> t1 = Triangle(1, [p1, p2, p3])
    """

    def __init__(self,ID=None, Points=[]):
        self.__points = Points
        if len(Points) == 3:
            self.__normal = self.normal_vec(Points)
        else:
            self.__normal = None
        self.__id = ID

    @staticmethod
    def normal_vec(points):
        p1 = points[0]
        p2 = points[1]
        p3 = points[2]
        # Defining two vectors and using cross product for normal vector
        p1_p2 = [p2.get_x()-p1.get_x(), p2.get_y() - p1.get_y(), p2.get_z() - p1.get_z()]
        p1_p3 = [p3.get_x() - p1.get_x(), p3.get_y() - p1.get_y(), p3.get_z() - p1.get_z()]
        norm_vec = np.cross(p1_p2, p1_p3)
        return norm_vec

    @property
    def id(self):
        return self.__id

    @ id.setter
    def id(self, ID):
        self.__id = ID

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points

    @property
    def normal(self):
        return self.__normal

    @normal.setter
    def normal(self, normal):
        self.__normal = normal

class Solid(object):
    """ A solid structure defined by triangles

    :param id(int): Solid ID
    :param triangles(list(Triangle)): List of all Triangles

    Example for creating a Tetrahedral-Solid out of triangles

    >>> t1 = Triangle(1, p1, p2, p3)
    >>> t2 = Triangle(2, p2, p3, p4)
    >>> t3 = Triangle(3, p3, p4, p1)
    >>> t4 = Triangle(4, p2, p4, p1)
    >>> s1 = Solid(1, [t1, t2, t3, t4])
    """

    def __init__(self,ID=None, Triangles=[]):
        self.__id = ID
        self.__triangles = Triangles

    @property
    def id(self):
        return self.__id

    @ id.setter
    def id(self, ID):
        self.__id = ID

    @property
    def triangles(self):
        return self.__triangles

    @triangles.setter
    def triangles(self, Triangles):
        if len(Triangles) == 0:
            raise ValueError ("No triangle were found for solid ", self.__id)


class Surface():

    def __init__(self):
        self.__triangles = []

    @property
    def triangles(self):
        return self.__triangles

    @triangles.setter
    def triangles(self, Triangles):
        self.__triangles = Triangles

    def create_surface_on_elements(self, elements):
        eFace = {} # Counts how many times is there a face
        for elem in elements:
            if len(elem.get_nodes()) == 8 or len(elem.get_nodes()) == 20:
                n1 = elem.get_nodes()[0].get_id()
                n2 = elem.get_nodes()[1].get_id()
                n3 = elem.get_nodes()[2].get_id()
                n4 = elem.get_nodes()[3].get_id()
                n5 = elem.get_nodes()[4].get_id()
                n6 = elem.get_nodes()[5].get_id()
                n7 = elem.get_nodes()[6].get_id()
                n8 = elem.get_nodes()[7].get_id()
                f = sorted([n1, n2, n3, n4])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face2
                f = sorted([n5, n8, n7, n6])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face3
                f = sorted([n1, n5, n6, n2])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face4
                f = sorted([n2, n6, n7, n3])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face5
                f = sorted([n3, n7, n8, n4])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face6
                f = sorted([n4, n8, n5, n1])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
            if len(elem.get_nodes()) == 6  or len(elem.get_nodes()) == 15:
                n1 = elem.get_nodes()[0].get_id()
                n2 = elem.get_nodes()[1].get_id()
                n3 = elem.get_nodes()[2].get_id()
                n4 = elem.get_nodes()[3].get_id()
                n5 = elem.get_nodes()[4].get_id()
                n6 = elem.get_nodes()[5].get_id()
                # Face1
                f = sorted([n1, n2, n3])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face2
                f = sorted([n4, n6, n5])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face3
                f = sorted([n1, n4, n5, n2])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face4
                f = sorted([n2, n5, n6, n3])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face5
                f = sorted([n3, n6, n4, n1])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1

            if len(elem.get_nodes()) == 4 or len(elem.get_nodes()) == 10:
                n1 = elem.get_nodes()[0].get_id()
                n2 = elem.get_nodes()[1].get_id()
                n3 = elem.get_nodes()[2].get_id()
                n4 = elem.get_nodes()[3].get_id()
                # Face1
                f = sorted([n1, n2, n3])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face2
                f = sorted([n1, n4, n2])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face3
                f = sorted([n2, n4, n3])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face4
                f = sorted([n3, n4, n1])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
        tn = 0
        for elem in elements:
            if len(elem.get_nodes()) == 8 or len(elem.get_nodes()) == 20:
                n1 = elem.get_nodes()[0].get_id()
                n2 = elem.get_nodes()[1].get_id()
                n3 = elem.get_nodes()[2].get_id()
                n4 = elem.get_nodes()[3].get_id()
                n5 = elem.get_nodes()[4].get_id()
                n6 = elem.get_nodes()[5].get_id()
                n7 = elem.get_nodes()[6].get_id()
                n8 = elem.get_nodes()[7].get_id()
                n11 = elem.get_nodes()[0]
                n22 = elem.get_nodes()[1]
                n33 = elem.get_nodes()[2]
                n44 = elem.get_nodes()[3]
                n55 = elem.get_nodes()[4]
                n66 = elem.get_nodes()[5]
                n77 = elem.get_nodes()[6]
                n88 = elem.get_nodes()[7]
                # Face1
                f = sorted([n1, n2, n3, n4])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n11, n22, n33])
                    self.triangles.append(tmp_tri)
                    tn += 1
                    tmp_tri = Triangle(tn, [n33, n44, n11])
                    self.triangles.append(tmp_tri)
                    tn += 1
                # Face2
                f = sorted([n5, n8, n7, n6])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n55, n88, n77])
                    self.triangles.append(tmp_tri)
                    tn += 1
                    tmp_tri = Triangle(tn, [n77, n66, n55])
                    self.triangles.append(tmp_tri)
                    tn += 1
                # Face3
                f = sorted([n1, n5, n6, n2])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n11, n55, n66])

                    self.triangles.append(tmp_tri)
                    tn += 1
                    tmp_tri = Triangle(tn, [n66, n22, n11])
                    self.triangles.append(tmp_tri)
                    tn += 1
                # Face4
                f = sorted([n2, n6, n7, n3])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n22, n66, n77])
                    self.triangles.append(tmp_tri)
                    tn += 1
                    tmp_tri = Triangle(tn, [n77, n33, n22])
                    self.triangles.append(tmp_tri)
                    tn += 1
                # Face5
                f = sorted([n3, n7, n8, n4])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n33, n77, n88])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n88, n44, n33])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face6
                f = sorted([n4, n8, n5, n1])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n44, n88, n55])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n55, n11, n44])
                    self.triangles.append(tmp_tri)
                    tn += 1

            if len(elem.get_nodes()) == 6 or len(elem.get_nodes()) == 15:
                n1 = elem.get_nodes()[0].get_id()
                n2 = elem.get_nodes()[1].get_id()
                n3 = elem.get_nodes()[2].get_id()
                n4 = elem.get_nodes()[3].get_id()
                n5 = elem.get_nodes()[4].get_id()
                n6 = elem.get_nodes()[5].get_id()
                n11 = elem.get_nodes()[0]
                n22 = elem.get_nodes()[1]
                n33 = elem.get_nodes()[2]
                n44 = elem.get_nodes()[3]
                n55 = elem.get_nodes()[4]
                n66 = elem.get_nodes()[5]
                # Face1
                f = sorted([n1, n2, n3])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n11, n22, n33])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face2
                f = sorted([n4, n6, n5])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n44, n66, n55])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face3
                f = sorted([n1, n4, n5, n2])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n11, n44, n55])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n55, n22, n11])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face4
                f = sorted([n2, n5, n6, n3])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n22, n55, n66])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n66, n33, n22])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face5
                f = sorted([n3, n6, n4, n1])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n33, n66, n44])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n44, n11, n33])
                    self.triangles.append(tmp_tri)
                    tn += 1

            if len(elem.get_nodes()) == 4 or len(elem.get_nodes()) == 10:
                n1 = elem.get_nodes()[0].get_id()
                n2 = elem.get_nodes()[1].get_id()
                n3 = elem.get_nodes()[2].get_id()
                n4 = elem.get_nodes()[3].get_id()
                n11 = elem.get_nodes()[0]
                n22 = elem.get_nodes()[1]
                n33 = elem.get_nodes()[2]
                n44 = elem.get_nodes()[3]
                # Face1
                f = sorted([n1, n2, n3])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n11, n22, n33])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face2
                f = sorted([n1, n4, n2])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n11, n44, n22])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face3
                f = sorted([n2, n4, n3])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n22, n44, n33])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face4
                f = sorted([n3, n4, n1])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n33, n44, n11])
                    self.triangles.append(tmp_tri)
                    tn += 1
