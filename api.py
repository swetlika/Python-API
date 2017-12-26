from flask import Flask, jsonify, request
import CreateGraph
import json

app = Flask(__name__)

# initialize data and graph
graph = CreateGraph.createGraph()

# test
@app.route('/')
def index():
    return jsonify({'Hello': 'World'})

'''
If given a name, filters out all actors that contain name
Else display all actors in the graph
'''
@app.route('/actors', methods=['GET'])
def actors_attr():
    actors = graph.get_actors()
    result = request.args.get('name')
    if result:
        result = ''.join(x for x in result if x.isalpha())
        res_actors = [x for x in actors if result in x]
        return jsonify({'movies': res_actors})

    return jsonify({'actors': actors})


'''
If given a name, filters out all movies that contain name
Else display all actors in the graph
'''
@app.route('/movies', methods=['GET'])
def movies_attr():
    movies = graph.get_movies()
    result = request.args.get('name')
    if result:
        result = ''.join(x for x in result if x.isalpha())
        res_movies = [x for x in movies if result in x]
        return jsonify({'movies': res_movies})


    return jsonify({'movies': movies})

'''
Returns the first Actor object that has the correct name
Displays actor attributes and metadata
'''
@app.route('/actors/<string:name>', methods=['GET'])
def return_actor(name):
    name = name.replace('_', ' ')
    v = graph.get_vertex(name)
    if v:
        ret = {
            'name': name,
            'age': v.get_info(),
            'gross income': v.get_income(),
        }
        return jsonify(ret)
    else:
        return jsonify({'actor': name + ' not found'})

'''
Returns the first Movie object that has correct name
Displays movie attributes and metadata
'''
@app.route('/movies/<string:name>', methods=['GET'])
def return_movie(name):
    name = name.replace('_', ' ')
    v = graph.get_vertex(name)
    if v:
        ret = {
            'name': name,
            'release year': v.get_info(),
            'gross income': v.get_income(),
        }
        return jsonify(ret)
    else:
        return jsonify({'movie' : name + ' not found'})

'''
Given a gross_income, update Actor object's income attribute in graph
'''
@app.route('/actors/<string:name>', methods=['PUT'])
def put_actor(name):
    total_gross = request.args.get('total_gross')
    name = name.replace('_', ' ')
    v = graph.get_vertex(name)
    v.set_income(total_gross)
    if v:
        ret = {
            'name': name,
            'age': v.get_info(),
            'gross income': v.get_income(),
        }
        return jsonify(ret)
    else:
        return jsonify({'actor': name + ' not found'})


'''
Given a box_office, update Movie object's income attribute in graph
'''
@app.route('/movies/<string:name>', methods=['PUT'])
def put_movie(name):
    box_office = request.args.get('box_office')
    name = name.replace('_', ' ')
    v = graph.get_vertex(name)
    v.set_income(box_office)
    if v:
        ret = {
            'name': name,
            'release year': v.get_info(),
            'box office': v.get_income(),
        }
        return jsonify(ret)
    else:
        return jsonify({'movie': name + ' not found'})


'''
Add a new Actor object to graph given a name
'''
@app.route('/actors/<string:name>', methods=['POST'])
def add_actor(name):
    name = name.replace('_', ' ')
    if name not in graph.get_actors():
        graph.add_vertex(name, type='Actor')
        actors = graph.get_actors()
        return jsonify({'actors': actors})

    else:
        return jsonify({'actor': name + ' already in actors list'})


'''
Add a new Movie object to graph given a name
'''
@app.route('/movies/<string:name>', methods=['POST'])
def add_movie(name):
    name = name.replace('_', ' ')
    if name not in graph.get_movies():
        graph.add_vertex(name, type='Movie')
        movies = graph.get_movies()
        return jsonify({'movies': movies})

    else:
        return jsonify({'movie': name + ' already in movies list'})


'''
Delete Actor object with the given name from graph
If that actor is currently in the graph
'''
@app.route('/actors/<string:name>', methods=['DELETE'])
def remove_actor(name):
    name = name.replace('_', ' ')
    if name in graph.get_actors():
        graph.remove_vertex(name)
        actors = graph.get_actors()
        return jsonify({'actors': actors})

    else:
        return jsonify({'actor': name + ' not found'})


'''
Delete Movie object with the given name from graph
If that actor is currently in the graph
'''
@app.route('/movies/<string:name>', methods=['DELETE'])
def remove_movie(name):
    name = name.replace('_', ' ')
    if name in graph.get_movies():
        graph.remove_vertex(name)
        movies = graph.get_movies()
        return jsonify({'movies': movies})

    else:
        return jsonify({'movie': name + ' not found'})


if __name__ == '__main__':
    app.run(debug=True, port = 5000)