from flask import Flask, render_template, request

import map_utils
from iris import get_table_head, get_simple_graph, get_iris_2d_graph, get_iris_3d_graph

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/home')
def get_home():  # put application's code here
    return render_template('index.html', title='Home Page')



@app.route('/about')
def get_about():  # put application's code here
    return render_template('about.html', title='About Page')


@app.route('/iris')
def get_iris():
    table = get_table_head()
    data1 = get_iris_2d_graph()
    data2 = get_iris_3d_graph()
    return render_template('iris.html', title='Iris Data', table=table, img_src='data:image/png;base64', graph1=data1, graph2=data2)


@app.route('/maps')
def get_maps():
    return render_template('maps.html', title='Maps')


@app.route('/simple_graph', methods=['GET'])
def get_simple_graph_page():
    start = 0
    end = 5
    if request.method == 'GET':
        if request.args.get('start') is not None:
            start = int(request.args.get('start'))
        if request.args.get('end') is not None:
            end = int(request.args.get('end')) + 1
    data = get_simple_graph([x**2 for x in range(start, end)], title="Simple Graph")
    return render_template('simple_graph.html', title='Simple Graph', img_src='data:image/png;base64', data=data)


@app.route('/full_map')
def get_fullmap():
    return map_utils.get_full_map()


@app.route('/political_map')
def get_political_map():
    return render_template('maps.html', title='Political', map=map_utils.get_political())


if __name__ == '__main__':
    app.run()
