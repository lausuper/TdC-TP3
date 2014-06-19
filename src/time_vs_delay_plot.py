#!/usr/bin/env python2
# coding: utf-8

import plot

class TimeVsDelayPlot(plot.Plot):

    def do_plot(self, plt, fig, db):
        colors = ['Green', 'DarkCyan', 'Indigo', 'Brown', 'DarkGoldenRod', 'Crimson',
                  'Orange', 'GreenYellow', 'DarkMagenta', 'MidnightBlue', 'DimGray']
        loss_probabilities = db.get_time_vs_delay_loss_probabilities()

        for loss in loss_probabilities:
            time_vs_delay = db.get_time_vs_delay(loss)

            data = time_vs_delay.items()
            data.sort()
            data = zip(*data)
            delays = [s * 1000 for s in data[0]]
            avgs = list(data[1])

            plt.plot(delays, avgs, color=colors.pop(), label=str(loss), lw=2)

        plt.xticks(delays, delays, fontsize=9, rotation=90)
        plt.xlim([delays[0], delays[-1]])
        plt.title(u'Tiempo de transferencia en función del retraso en envío de ACKs')
        plt.xlabel(u'Retraso en envío de ACKs (ms)')
        plt.ylabel(u'Tiempo de transferencia promedio (s)')
        plt.legend(loc=2)

if __name__ == '__main__':
    TimeVsDelayPlot()