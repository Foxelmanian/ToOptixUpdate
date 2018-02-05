

class Node(object):
    """ An node object with x,y,z and id

    """

    def __init__(self, node_id: int, x: float, y: float, z: float):

        self.__id = node_id
        self.__x = x
        self.__y = y
        self.__z = z

    def __str__(self):
        return ('ID: {} Coordinates: {}, {}, {}'.format(
            self.__id, self.__x, self.__y, self.__z))

    def get_x(self) -> float:
        return self.__x

    def set_x(self, x: float):
        self.__x = x


if __name__ == "__main__":
    n1 = Node(1, 1.0, 2, 3)
    print(n1)
    n1.set_x(3.0)
