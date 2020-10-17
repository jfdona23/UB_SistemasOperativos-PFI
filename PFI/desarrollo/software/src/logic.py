import subprocess
import csv
import os
from typing import OrderedDict
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
        Consume the CSV file with IRQ data and timings and returns a list of dictionaries
        containing the irq data parsed from the CSV

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
                else:
                    return badFile
            return goodFile

    def cleanFiles(self):
        toRemove = Path(self.uploadsDirectory).iterdir()
        for r in toRemove:
            os.remove(r)
        return
                    
    def processAll(self):
        """
        Process the CSV and generates a Gantt graph.
        It returns a list of dictionaries containing the irq data parsed from the CSV
        """
        irqData = self.__parseCSV(self.__pickUpLastCreatedFile(self.uploadsDirectory))
        # Create the plot
        matplotlib.use('agg')       # Interactive mode OFF / Write to file
        fig, gantt = plt.subplots()   # Declaring a figure (fig) and an array of axes (gantt)
        # Start the action, aka Gantt population
        ladder = 1
        limX = 1
        limY = 0
        for i in irqData:
            n = i.get('name')
            t = int(i.get('trigger'))
            d = int(i.get('duration'))
            q = int(i.get('quantum'))
            if d > q:
                frags = d // q
                lastFrag = d % q
                for i in range(0,frags):
                    gantt.broken_barh([(t, q)], (ladder, 1), facecolors=('tab:blue'), label=n)
                    gantt.broken_barh([(t + q, 1)], (ladder + 1, 1), facecolors='grey', label='OV')
                    t = t + q + 1
                if lastFrag > 0:
                    gantt.broken_barh([(t, lastFrag)], (ladder, 1), facecolors=('tab:blue'), label=n)
                    gantt.broken_barh([(t + lastFrag, 1)], (ladder + 1, 1), facecolors='grey', label='OV')
            else:
                gantt.broken_barh([(t, d)], (ladder, 1), facecolors=('tab:blue'), label=n)
                gantt.broken_barh([(t + q, 1)], (ladder + 1, 1), facecolors='grey', label='OV')
            limX += t
            limY += 1
            ladder += 2
        limY *= 3   # By 3 in order to get some extra space

        ## -- Start Gantt graph Settings -- ##
        fig.tight_layout()
        fig.subplots_adjust(top=0.90)
        fig.suptitle('Diagrama de Interrupciones', fontsize=14)
        gantt.grid(True)
        gantt.set_xlabel('Ciclos')
        gantt.set_ylabel('Procesos')
        gantt.set_ylim(0, limY)
        gantt.set_xlim(0, limX)
        # Dynamically set the X ticks
        ticks = [x for x in range(0,limX + 1)]
        gantt.set_xticks(ticks)
        # handle duplicated labels
        handles, labels = plt.gca().get_legend_handles_labels()
        byLabel = OrderedDict(zip(labels, handles))
        gantt.legend(byLabel.values(), byLabel.keys(), loc="best")
        ## -- End Gantt graph Settings -- ##
        
        # Tune the colors prior saving
        # gantt.spines['bottom'].set_color('white')
        # gantt.spines['top'].set_color('white') 
        # gantt.spines['right'].set_color('white')
        # gantt.spines['left'].set_color('white')
        # gantt.tick_params(axis='x', colors='white')
        # gantt.tick_params(axis='y', colors='white')
        # gantt.yaxis.label.set_color('white')
        # gantt.xaxis.label.set_color('white')
        # gantt.title.set_color('white')
        # Save the file to disk
        plt.savefig("static/output.png", transparent=False)

        i = irqData if len(irqData) > 0 else None
        return i


if __name__ == "__main__":
    pass