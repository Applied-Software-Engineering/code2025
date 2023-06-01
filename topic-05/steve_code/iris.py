import base64
import os
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA


def get_plot_data(plot):
    """
    This function creates an image in memory of a matplotlib plot
    :param plot:
    :return:
    """
    # Save it to a temporary buffer.
    buf = BytesIO()
    plot.savefig(buf, format="png")
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")

# SIMPLE GRAPH

def get_simple_graph(plot_data, title=None):
    # clear the plot
    plt.clf()
    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.subplots()
    if title:
        ax.set_title(title)
    ax.plot(plot_data)
    return get_plot_data(fig)

# IRIS DATA


def get_iris_df():
    return pd.read_csv(os.path.join('res', 'iris.csv'))


def get_table_head():
    return get_iris_df().head().to_html()


def get_iris_2d_graph():
    df = get_iris_df()
    plt.clf()
    plt.figure(2, figsize=(8, 6))
    plt.title("Iris Dataset (2d) Scatter graph")
    # data.columns -> Index(['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species'],
    # dtype='object')
    plt.xlabel(df.columns[1])
    plt.ylabel(df.columns[2])

    x1 = df.iloc[:, 1]  # SepalLengthCm
    x2 = df.iloc[:, 2]  # SepalWidthCm
    species_mapping = {"Iris-setosa": 0, "Iris-versicolor": 1, "Iris-virginica": 2}
    y = [species_mapping.get(item) for item in df.loc[:, 'Species']]
    plt.scatter(x1, x2, c=y)
    return get_plot_data(plt)


def get_iris_3d_graph():
    df = pd.read_csv(os.path.join('res', 'Iris.csv'))
    plt.clf()
    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d", elev=-150, azim=110)
    iris_data = np.array(df.iloc[:, 1:5].values.tolist())

    species_mapping = {"Iris-setosa": 0, "Iris-versicolor": 1, "Iris-virginica": 2}
    y = [species_mapping.get(item) for item in df.loc[:, 'Species']]

    X_reduced = PCA(n_components=3).fit_transform(iris_data)
    ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=y, cmap=plt.cm.Set1, edgecolor="k", s=40, )

    ax.set_title("First three PCA directions")
    ax.set_xlabel("1st eigenvector")
    ax.xaxis.set_ticklabels([])
    ax.set_ylabel("2nd eigenvector")
    ax.yaxis.set_ticklabels([])
    ax.set_zlabel("3rd eigenvector")
    ax.zaxis.set_ticklabels([])
    return get_plot_data(plt)



if __name__ == "__main__":
    pass