# import matplotlib.pyplot as plt
# import matplotlib as mpl

# def plot_route(route):
#     """ Plots found route """
#     ax = route.plot.scatter(
#             x='x',
#             y='y',
#             c='DarkBlue'
#         )

#     for index, row in route.iterrows():
#         if index != len(route) - 1:
#             vertice = route.loc[[index, index+1]]
#             plt.plot(vertice['x'].tolist(), vertice['y'].tolist(), 'ro-')
#     plt.show()