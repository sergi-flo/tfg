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


def mutliplot(d,do):
  pass

if  __name__=='__main__':
  x=['a','b','r','t','g']
  y=[7,9,6,3,12]
  graphic(x,y)
