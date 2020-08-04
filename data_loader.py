import pandas
import numpy as np

class DataLoader:

  def read_csv(self,filename):
    data = pandas.read_csv("./data/"+filename, index_col=0)
    y = data.values
    x = data.index
    labels=data.columns.values
    return x, y, labels

  def get_data(self, datasets=['simulatedflowdata.csv', 'observedflowdata.csv']):
    '''
    Load two datasets by name and estimate difference between two.
    I'm using % difference here, but any other kind works.
    NEED TO IMPLEMENT: check for differences in x and labels between the two datasets

    :param datasets: list of csv filenames to load and plot difference
    :return: x-axis labels, difference (y), and labels for each panel
    '''
    x1, y1, labels1 = self.read_csv(datasets[0])
    x1, y2, labels2 = self.read_csv(datasets[1])

    y_diff = np.divide(y1-y2,y2, out=np.zeros_like(y2,dtype=float), where=y2!=0)

    return x1,y_diff, labels1

