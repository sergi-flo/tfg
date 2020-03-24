#!/usr/bin/env python3

import matplotlib.pyplot as plt

def graphic(x,y):
  x_pos=[i for i,_ in enumerate(x)]
  plt.bar(x_pos,y)
  plt.xticks(rotation=90)
  plt.title('Primer grafico')
  plt.xlabel('Sensors')
  plt.ylabel('Valors')
  plt.xticks(x_pos,x)
  plt.tick_params(labelsize=5, labelrotation=90, width=0.8)
  plt.show()
 
def dic_to_data(d):
  x=[]
  y=[]
  for sensor in d:
    x.append(sensor)
    median=sum([float(e) for e in d[sensor]])/len(d[sensor])
    y.append(median)
  return x,y


def multiplot(d,do):
  fig, axs =plt.subplots(len(d),len(do), sharex=True, sharey=True)
  c=0
  for e in d:
    c1=c
    for e1 in d:
      axs.flat[c1].set(xlabel=e1,ylabel=e)
      #if d[e]==d[e1]:
      #  axs[c,c1].bar(d[e],d[e1],'tab:orange')
      #  axs[c,c1].bar(do[e],do[e1],'tab:blue')
      axs[c,c1].scatter(d[e],d[e1],'tab:orange')
      axs[c,c1].scatter(do[e],do[e1],'tab:blue')
      c1+=1
    c=c1
  for ax in axs.flat:
    ax.label_outer()
  plt.show()

if  __name__=='__main__':
  #x=['a','b','r','t','g']
  #y=[7,9,6,3,12]
  #graphic(x,y)
  d={'Amplitude': [], 'Oscillations': [], 'Inst freq': []}
  do={'Amplitude': [], 'Oscillations': [], 'Inst freq': []}
  multiplot(d,do)
