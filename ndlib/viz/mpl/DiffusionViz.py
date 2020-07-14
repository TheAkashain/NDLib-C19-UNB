import abc
from bokeh.palettes import Category20_9 as cols
import os
import matplotlib as mpl
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
import future.utils
import six

__author__ = 'Giulio Rossetti'
__license__ = "BSD-2-Clause"
__email__ = "giulio.rossetti@gmail.com"


@six.add_metaclass(abc.ABCMeta)
class DiffusionPlot(object):
   # __metaclass__ = abc.ABCMeta

    def __init__(self, model, trends):
        self.model = model
        self.trends = trends
        statuses = model.available_statuses
        self.srev = {v: k for k, v in future.utils.iteritems(statuses)}
        self.ylabel = ""
        self.title = ""
        self.nnodes = model.graph.number_of_nodes()
        self.normalized = True

    @abc.abstractmethod
    def iteration_series(self, percentile):
        """
        Prepare the data to be visualized

        :param percentile: The percentile for the trend variance area
        :return: a dictionary where iteration ids are keys and the associated values are the computed measures
        """
        pass

    def plot(self, filename=None, percentile=90, statuses=None, itercount = None, timereq = None):
        """
        Generates the plot

        :param filename: Output filename
        :param percentile: The percentile for the trend variance area
        :param statuses: List of statuses to plot. If not specified all statuses trends will be shown.
        """

        pres = self.iteration_series(percentile)
        # infos = self.model.get_info()
        # descr = ""

        plt.figure(figsize=(20, 10))
        ax = plt.subplot()

        # for k, v in future.utils.iteritems(infos):
        #     descr += "%s: %s, " % (k, v)
        # descr = descr[:-2].replace("_", " ")

        mx = 0
        i = 0
        for k, l in future.utils.iteritems(pres):

            if statuses is not None and self.srev[k] not in statuses:
                continue
            mx = len(l[0])
            if self.normalized:
                plt.plot(list(range(0, mx)), l[1]/self.nnodes, lw=2, label=self.srev[k], alpha=0.5)  # , color=cols[i])
                plt.fill_between(list(range(0,  mx)), l[0]/self.nnodes, l[2]/self.nnodes, alpha=0.2)
                    #,color=cols[i])
            else:
                plt.plot(list(range(0, mx)), l[1], lw=2, label=self.srev[k], alpha=0.5)  # , color=cols[i])
                plt.fill_between(list(range(0, mx)), l[0], l[2], alpha="0.2")  # ,color=cols[i])

            i += 1

        plt.grid(axis="y")
        # plt.title(descr)
        plt.xlabel("Time (Days)", fontsize=24)
        plt.ylabel("Percent of Population", fontsize=24)
        plt.legend(loc="best", fontsize=18)
        plt.xlim((0, mx))
        if (itercount is not None) and (timereq is not None):
            ax.text(0.75, 0.25, 'Number of Simulations: {} \nExecution Time: %.3f seconds'.format(itercount) % (timereq), fontsize = 18,
                     bbox = dict(boxstyle = 'round', facecolor = 'white'), transform = ax.transAxes)
        elif itercount is not None:
            ax.text(0.75, 0.25, 'Number of Simulations: {}'.format(itercount),fontsize = 18, 
                     bbox = dict(boxstyle = 'round', facecolor = 'white'), transform = ax.transAxes) 
        elif timereq is not None:
            ax.text(0.75, 0.25, 'Execution Time: {}'.format(timereq), fontsize = 18,
                     bbox = dict(boxstyle = 'round', facecolor = 'white'), transform = ax.transAxes)
        plt.tight_layout()
        if filename is not None:
            plt.savefig(filename)
            plt.clf()
        else:
            plt.show()
