"""
A vertex of a graph represents each point It holds information about the actor/movie,
including the name, info (which is the release year of a movie, and the age of an actor),
and the type, which is True if movie, else False
"""

class Vertex:
    def __init__(self, node, info=0, income=0, type='None'):
        self.id = node
        self.type = type

        # if vertex is a movie, info = info movie was released
        # if vertex is an actor, info = age of actor
        self.info = info

        # stores total income of actor/movie
        self.income = income
        self.neighbors = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.neighbors])

    # while adding an edge between a vertex and another, add the other one to this vertex's neighbor list
    # edges are weighted
    def add_neighbor(self, neighbor, weight=0):
        self.neighbors[neighbor] = weight

    # returns a list of all the adjacent vertices of the current
    def get_neighbors(self):
        return self.neighbors.keys()

    # returns movie title if type movie
    # returns actor name if type actor
    def get_id(self):
        return self.id

    # returns the weight of the edge
    def get_weight(self, neighbor):
        return self.neighbors[neighbor]

    # returns release year if movie
    # returns age of actor if actor
    def get_info(self):
        return self.info

    # returns income of the movie/actor
    def get_income(self):
        return self.income

    def set_income(self,income):
        self.income = income

    # returns True if type movie
    # returns False if type actor
    def get_type(self):
        return self.type