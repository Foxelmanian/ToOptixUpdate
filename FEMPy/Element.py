from typing import List

"""


"""


class Element(object):
    """ This class is used for creating a element of FEM
    """

    def __init__(self, element_id: int, nodes: List[int]):
        self.__nodes = nodes
        self.__element_id = element_id

    def get_id(self) -> int:
        return self.__element_id






