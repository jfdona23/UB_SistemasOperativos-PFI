import subprocess
import csv
import os
import plotly.express as px
import pandas as pd
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
        print(irqData)

        df = pd.DataFrame([
        dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
        dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
        dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')
        ])

        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
        fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
        fig.show()

        i = irqData[0] if len(irqData) > 0 else None
        return i


if __name__ == "__main__":
    pass