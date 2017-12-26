from Vertex import Vertex
from Graph import Graph
import datetime
import logging
import json
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx




'''
gets all the movies from Wikipedia's List of Highest Grossing Films
:returns a list of movie tuples in the form (movie title, movie wikipedia url, gross income, release year)
'''
def get_movies(data):
    movies = []

    for movie in data[1]:
        gross_income = data[1][movie]['box_office']
        release_year = data[1][movie]['year']
        movies.append((movie, gross_income, release_year))

    return movies


'''
Finds all the actors from the highest grossing films wikipedia page
by visiting each movie's url and scraping the infobox for the cast
:return List of (actors, income from given movie)
'''
def get_actors(movie, data):
    actors = []
    try:
        for actor in data[1][movie]['actors']:
            age = data[0][actor]['age']
            income = data[0][actor]['total_gross']
            actors.append((actor, income, age))
    except:
        logging.error('actor not found')

    return actors


'''
Create a graph of all the data scraped
vertices are the movies and actors
a movie has edges to each of its cast members
an actor has an edge to another actor he/she worked with
'''
def createGraph():
    logging.info('Starting creating graph ' + str(datetime.datetime.now()))

    with open('data.json') as file:
        data = json.load(file)

    movie_collection = get_movies(data)
    g = Graph()

    for movie_item in movie_collection:
        # movie = tuple of (movie_title, movie_url, gross_income, movie_release_year)
        movie_title = movie_item[0]
        gross_income = movie_item[1]
        movie_release_year = movie_item[2]

        # add movie vertex to graph
        # type_is_movie is True since this is a movie
        g.add_vertex(movie_title, movie_release_year, gross_income, 'Movie')

        # get list of the cast of the movie
        actors = get_actors(movie_title, data)

        for actor_item in actors:
            # actor = tuple of (actor name, income from that movie, age)
            actor = actor_item[0]
            actor_income = actor_item[1]
            actor_age = actor_item[2]


            # add actor to graph
            # type_is_movie is False since this is an actor
            if actor not in g.get_vertices():
                g.add_vertex(actor, actor_age, actor_income, 'Actor')

            # add edge from actor to the movie
            # weight = income actor earned from movie
            g.add_edge(actor, actor_age, actor_income, 'Actor', movie_title, movie_release_year, gross_income, 'Movie', actor_income)

            # create edge from actor to rest of movie's cast
            # weight = 0 for actor to actor edges
            for edge_actor_item in actors:
                if edge_actor_item[0] != actor_item[0]:
                    edge_actor = edge_actor_item[0]
                    edge_income = edge_actor_item[1]
                    edge_age = edge_actor_item[2]

                    g.add_edge(actor, actor_age, actor_income, 'Actor', edge_actor, edge_age, edge_income, 'Actor', 0)

    logging.info('Finished creating graph ' + str(datetime.datetime.now()))
    return g


# returns Pearson correlation given a dictionary
# where x's = the keys and y's = the values of the dictionary
def get_correlation_from_dict(d):
    x = [x[0] for x in d]
    y = [y[1] for y in d]
    return np.corrcoef(x,y)[0][1]

def graph_hub_actors(d):
    x_names = [x[0] for x in d]
    x = range(len(d))
    y = [int(y[1]) for y in d]

    plt.scatter(x, y)
    plt.xticks(x, x_names, rotation='vertical')
    plt.title('Hub Actors')
    plt.xlabel('Actors')
    plt.ylabel('Number of Connections')

    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    plt.tight_layout()


    return plt


def graph_highest_grossing_ages(d):
    x = [x[0] for x in d]
    y = [y[1] for y in d]

    correlation = get_correlation_from_dict(d)

    plt.scatter(x, y)
    plt.title('Actor Age vs Grossing Income')
    plt.xlabel('Actors')
    plt.ylabel('Grossing Income')
    plt.text(2, 6, correlation, fontsize=15)

    return plt


'''
Takes in the graph created and displays the nodes and edges
'''
def visualize_graph(graph):
    out = nx.Graph()

    edges = []
    val_map = {}
    nodes = list(graph.get_vertices())[:10]
    for g in nodes:
        v = graph.get_vertex(g)
        if v.get_type() == "Actor":
            temp = v.get_id()
            out.add_node(temp)
        else:
            temp = v.get_id()
            out.add_node(temp)
            val_map[temp] = "magenta"
        for a in v.get_neighbors():
            if a.get_type() == "Actor":
                temp = a.get_id()
                out.add_node(temp)
            else:
                temp = a.get_id()
                out.add_node(temp)
                val_map[temp] = "goldenrod"
            edges.append((v.get_id(), temp))
    out.add_edges_from(edges)
    values = [val_map.get(node,"darkmagenta") for node in out.nodes()]

    pos = nx.spring_layout(out, scale=10)
    nx.draw_networkx(out, pos=pos, node_color = values, font_size = 5, node_size = 500, linewidths=2.0)

    return plt

graph = createGraph()
print(graph.get_hub_actors()[:25])
print(graph.highest_grossing_ages()[:25])