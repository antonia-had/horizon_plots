import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from data_transformer import DataTransformer

class InputError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return rep(self.value)

class Horizon:

  # public methods

  def run(self, x, y, labels, figsize=(15,20), bands=3, colors=("#8BBCD4","#2B7ABD","#0050A0","#EF9483","#E02421", "#A90E0A")): # dark blue, medium blue, light blue, dark red, medium red, light red
    """ Return the entire graph and its plt object

        Look at DataTransformer.transform to see how the data is transformed.

        Keyword arguments:
        x: single array with x values. Distance between neighboring entries have to be the same
        y: two-dimensional array with y values for each entry.
        labels: array with strings, shown as the labels on the y-axis.
        figsize: (a,b) used when creating the figure (optional)
        bands: default is 3
        colors: array with the colors used for the bands. from dark to light blue, then from dark red to light red.

        Requirements:
        len(y[i]) == len(x) for all 0 <= i < len(y)
        len(y[0]) == len(labels)
        len(colors) == 2*bands

        RETURN: plt object
    """

    self.check_valid_params(x,y,labels,figsize,bands,colors) 
    n = len(y[0,:])

    F, axes = plt.subplots(n, 1, figsize=figsize, sharex=True, sharey=True)
    df = DataTransformer(y, bands)

    for i, ax in enumerate(axes.flatten()):
      transformed_x, ybands = df.transform(y[:,i], x)
      for idx,band in enumerate(ybands):
        ax.fill_between(transformed_x[idx],0,band,color=colors[idx])
      self.adjust_visuals_line(x, df, ax, i, n, labels)

    F.text(0.5, 0.04, 'Time', ha='center', size=30)
    F.text(0.04, 0.5, 'Error to observation ratio', va='center', rotation='vertical', size=30)
    handles = []
    legend_colors=["#A90E0A", "#E02421", "#EF9483","#8BBCD4", "#2B7ABD", "#0050A0"]
    for c in legend_colors:
      handles.append(self.patch_creator(c))
    bandwidths = int(df.max)/bands
    lowerbounds = np.arange(int(df.min), int(df.max),bandwidths )
    labels = [str(int(b))+' - '+str(int(b+bandwidths)) for b in lowerbounds]
    F.legend(handles, labels, ncol=bands*2, loc='upper center',fontsize='xx-large')
    return plt

  # private methods
  def patch_creator(self, color):
    patch = mpatches.Rectangle((0, 0), 1, 1, fc=color)
    return patch
  #def set_theme(self,ax):
    # """ hides all ticks and labels on both axes """
    # ax.get_yaxis().set_visible(False)
    # ax.get_xaxis().set_visible(False)

    
  def adjust_visuals_line(self, x, df, ax, i, n, labels):
    """ adjusts the subplot: height, width, labels """
    plt.xlim(0, x[-1])
    plt.ylim(0, df.get_max()/3)
    #self.set_theme(ax)
    ax.set_yticks([])
    ax.set_title(labels[i])
    ax.set_xticks([])
    if i==0:
      ax.set_yticks(np.arange(0, 100, 20))
    if i==n-1:
      ax.set_xticks(np.arange(0,len(x),12*5))
      ax.set_xticklabels(np.arange(1975,2013,5), size=18) # these are specific to the example and need to be changed
    
  def check_valid_params(self, x,y,labels, figsize, bands, colors):
    """ checks parameters, throws an InputError if parameters are invalid """

    if bands * 2 != len(colors):
      raise InputError("Number of bands invalid for number of colors")

    if len(y[0,:]) != len(labels):
      raise InputError("Lengths of arrays y and labels are different")

    if len(x) != len(y[:,0]):
      raise InputError("Lengths of arrays x and y are different")
