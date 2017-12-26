import unittest
from CreateGraph import *


class TestStringMethods(unittest.TestCase):

    logging.basicConfig(filename='create_graph.log', level=logging.DEBUG)
    logging.debug('This message should go to the log file')

    graph = createGraph()


    def test_hub_actors(self):
        hub_actors = self.graph.get_hub_actors()

        # clear previous plt graphs
        plt.clf()
        plt.cla()
        plt.close()

        # graph top 25 hub actors
        plt1 = graph_hub_actors(hub_actors[:25])
        plt1.savefig('outputs/actor_connections.pdf')

        self.assertEquals(hub_actors[0][0], 'Bruce Willis')


    def test_highest_grossing_ages(self):
        highest_grossing_ages = self.graph.highest_grossing_ages()

        # clear previous plt graphs
        plt.clf()
        plt.cla()
        plt.close()

        # graph income vs ages
        plt2 = graph_highest_grossing_ages(highest_grossing_ages)
        plt2.savefig('outputs/age_vs_income.pdf')

        self.assertEquals(highest_grossing_ages[0][0], 61)


    def test_graph_visualization(self):
        # clear previous plt graphs
        plt.clf()
        plt.cla()
        plt.close()

        # show small subset of graph visualization
        plt3 = visualize_graph(self.graph)
        plt3.savefig('outputs/visualization.pdf')




if __name__ == '__main__':
    unittest.main()




