# coding: utf-8

import sys
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

from database import DB


class Plot:
    def __init__(self):
        # Read and validate command-line arguments
        if len(sys.argv) != 1 and len(sys.argv) != 3:  sys.exit(self.help())
        if len(sys.argv) == 3 and sys.argv[1] != '-o': sys.exit(self.help())
        output_path = sys.argv[2] if len(sys.argv) == 3 else None

        plt.rcParams['text.latex.preamble']=[r'\usepackage{lmodern}']
        plt.rcParams.update({'text.usetex':        True,
                             'text.latex.unicode': True,
                             'font.family':        'lmodern',
                             'font.size':          10,
                             'axes.titlesize':     10})

        fig = plt.figure()

        db = DB()
        self.do_plot(plt, fig, db)

        plt.tight_layout()

        if output_path is not None:
            plt.savefig(output_path, dpi=1000, box_inches='tight')
        else:
            plt.show()

    def help():
        return 'Usage: %s            Produces an on-screen interactive graph from standard input data.\n' \
               '       %s -o [path]  Saves the graph to [path].\n' \
               % (sys.argv[0], sys.argv[0])

    def do_plot(self, plt, fig, db):
        raise NotImplementedError