import subprocess
import csv
import os
# import plotly
# import plotly.express as px
# import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

class IRQAppLogic():
    """
    Logic happening behind the scenes
    """
    def __init__(self, uploadsDirectory):
        self.uploadsDirectory = uploadsDirectory

    def showInterruptStats(self):
        """
        Gather the IRQ stats from /proc/interrupts from a Unix like system.
        It returns the stdout whatever it is.
        """
        result = subprocess.run(['cat', '/proc/interrupts'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def __pickUpLastCreatedFile(self, dir):
        files = sorted(Path(dir).iterdir(), key=os.path.getctime, reverse=True)
        f = files[0] if len(files) > 0 else None
        return f

    def __parseCSV(self, file):
        """
        Consume the csv file with IRQ data and timings and produce a pythonic output

        File columns are as follow:
        0- Name
        1- Non maskable (0) / maskable (1)
        2- priority 1-100 being "1" the highest one
        3- Triggering (cicle of occurence)
        4- Duration (cicles)
        5- Quantum
        """
        goodFile = []
        badFile = [{'name':      'null',
                   'mask':      -1,
                   'priority':  -1,
                   'trigger':   -1,
                   'duration':  -1,
                   'quantum':   -1}]
        if file == None:
            return badFile
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) == 6:
                    goodFile.append({'name':     row[0],
                                     'mask':     row[1],
                                     'priority': row[2],
                                     'trigger':  row[3],
                                     'duration': row[4],
                                     'quantum':  row[5]})
                else:
                    return badFile
            return goodFile
                    
    def processAll(self):
        irqData = self.__parseCSV(self.__pickUpLastCreatedFile(self.uploadsDirectory))

        # df = pd.DataFrame([
        #     dict(Task="Job A", Start='2020-11-01', Finish='2020-11-8'),
        #     dict(Task="Job A", Start='2020-11-11', Finish='2020-11-20'),
        #     dict(Task="Job B", Start='2020-11-08', Finish='2020-11-10')
        # ])

        # fig = px.timeline(df,
        #                   x_start="Start",
        #                   x_end="Finish",
        #                   y="Task",
        #                   color="Task",
        #                   hover_data={"Task": True,
        #                               "Start": False,
        #                               "Finish": False})
        # fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
        # fig.update_xaxes(tickformat="1")
        # plotly.offline.plot(fig, filename='static/out.html')

        # Interactive mode OFF / Write to file
        matplotlib.use('agg')
        # Declaring a figure (fig) and an array of axis (gantt)
        fig, gantt = plt.subplots()
        # Setting Y-axis limits 
        gantt.set_ylim(0, 50)
        # Setting X-axis limits 
        gantt.set_xlim(0, 160)
        # Setting labels for x-axis and y-axis 
        gantt.set_xlabel('seconds since start')
        gantt.set_ylabel('Processor')
        # Setting ticks on y-axis 
        gantt.set_yticks([15, 25, 35]) 
        # Labelling tickes of y-axis 
        gantt.set_yticklabels(['1', '2', '3']) 
        # Setting graph attribute 
        gantt.grid(True) 
        # Declaring a bar in schedule 
        gantt.broken_barh([(40, 50)], (30, 9), facecolors =('tab:orange')) 
        # Declaring multiple bars in at same level and same width 
        gantt.broken_barh([(110, 10), (150, 10)], (10, 9), 
                                facecolors ='tab:blue') 
        gantt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9), 
                                        facecolors =('tab:red')) 
        plt.savefig("static/output.png")

        i = irqData[0] if len(irqData) > 0 else None
        return i


if __name__ == "__main__":
    pass