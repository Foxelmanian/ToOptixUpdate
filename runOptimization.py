from FEMPy.FEMBody import FEMBody
from FEMPy.CCXPhraser import CCXPhraser


def perform_topology_optimization(testFile):
    # Import Model
    FEM_builder = CCXPhraser(testFile)
    fem_body = FEM_builder.get_fem_body()

    # Start optimization process











if __name__ == "__main__":
    testFile = "FEMPy/example.inp"

    perform_topology_optimization(testFile)
