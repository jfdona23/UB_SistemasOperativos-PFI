import subprocess
import csv
import os
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
        badFile = [{'name': 'null', 'mask': -1, 'priority': -1, 'trigger': -1, 'duration': -1, 'quantum': -1}]
        if file == None:
            return badFile
        with open(file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) == 6:
                    goodFile.append(row)
                    print(row)
                else:
                    return badFile
            return goodFile
                    
    def processAll(self):
        irqData = self.__parseCSV(self.__pickUpLastCreatedFile(self.uploadsDirectory))

        matplotlib.use('agg')   # Interactive mode OFF / Write to file
        fig, gantt = plt.subplots() # Declaring a figure (fig) and an array of axis (gantt)
        gantt.set_ylim(0, 5)
        gantt.set_xlim(0, 160)
        gantt.set_xlabel('Ciclos')
        gantt.set_ylabel('Procesos')
        # Setting ticks on y-axis 
        # gantt.set_yticks([15, 25, 35])
        # Labelling ticks of y-axis 
        # gantt.set_yticklabels(['1', '2', '3'])
        gantt.grid(True) 
        gantt.broken_barh([(40, 50)], (3, 1), facecolors =('tab:orange')) 
        gantt.broken_barh([(110, 10), (150, 10)], (1, 1), facecolors ='tab:blue') 
        gantt.broken_barh([(10, 50), (100, 20), (130, 10)], (2, 1), facecolors =('tab:red')) 
        plt.savefig("static/output.png")

        i = irqData if len(irqData) > 0 else None
        return i


if __name__ == "__main__":
    pass