#!/usr/bin/env python3

import pandas as pd
import plotly.graph_objects as go

def load_panda():
  d=pd.read_csv('excel/hfos_final.csv')
  labels=[i for i in d]
  return d[labels[1:]]

def pand():
  out,noOut= 0,0
  d=load_panda()
  #print(data[data.columns[0]])
  #print(data)
  for e in d['Zone']:
    if 'Outside' in e:
      out +=1
    else:
      noOut +=1
  total=out+noOut
  print(out, noOut, total)

def patients():
  d=load_panda()
  patients_list=[]
  for patient in d['Patient']:
    if patient not in patients_list:
      patients_list.append(patient)
  return patients_list

def pand_sensores(selected_patient):
  dic={}
  d=load_panda()
  for amplitude, patient, channel in zip(d['Amplitude'],d['Patient'],d['Channel']):
    if selected_patient in patient:
      if channel in dic:
        dic[channel].append(amplitude)
      else:
        dic[channel] = [amplitude]
  #print(dic, len(dic))
  return dic

def dic_to_data(d):
  x=[]
  y=[]
  for sensor in d:
    x.append(sensor)
    median=sum([float(e) for e in d[sensor]])/len(d[sensor])
    y.append(median)
  return x,y

def multiplot_soz(selected_patient, *args):
  d=load_panda()
  filtered_d=d.loc[d['Patient']==selected_patient]
  dic={'Zone':[]}
  for zone in filtered_d['Zone']:
    if 'Outside' in zone:
      dic['Zone'].append(0)
    else:
      dic['Zone'].append(1) 
  for e in args:
    dic[e]=[]
    for row_zone, row_e in zip(filtered_d['Zone'], filtered_d[e]):
      if 'Propagation' in row_zone:
        pass
      else:
        dic[e].append(row_e)
  return dic


def multiplot_soz1(selected_patient, selector, args):
  d=load_panda()
  filtered_d=d.loc[d['Patient']==selected_patient]
  a=[]
  res=[]
  for e in d[selector]:
      if e not in a:
          d={0:e}
          for h in args:
            d[h]=[]
          res.append(d)
          a.append(e)
  for y in args:
    for e in res:
      for row_selector, row_e in zip(filtered_d[selector], filtered_d[y]):
        if row_selector == e[0]:
          e[y].append(row_e)
  return res

def scatter_soz1(selected_patient, selector, args): #args=[x,y]
  d=load_panda()
  filtered_d=d.loc[d['Patient']==selected_patient]
  a=[]
  res=[]
  for e in d[selector]:
      if e not in a:
          res.append({0:e, 'x':[], 'y':[]})
          a.append(e)
  for e in res:
    for row_selector, row_e in zip(filtered_d[selector], filtered_d[args[0]]):
      if row_selector == e[0]:
        e['x'].append(row_e)
  for e in res:
    for row_selector, row_e in zip(filtered_d[selector], filtered_d[args[1]]):
      if row_selector == e[0]:
        e['y'].append(row_e)
  return res

def mp(selected_patient, selector, values):
  x=multiplot_soz1(selected_patient, selector, values)
  print(x)
  data=[]
  for e in x:
    d=go.Splom(
    dimensions=[dict(label=k,values=e[k]) for k in e if k != 0],
    name=e[0],
    marker=dict(size=4),
    diagonal=dict(visible=False))
    data.append(d)
  print(data)
  layout=go.Layout(title="Multiplot prove", dragmode='select', hovermode='closest', showlegend=True)
  fig=go.Figure(data=data,layout=layout)
  return fig

def scatter(selected_patient, selector, values):
  x=scatter_soz1(selected_patient, selector, values)
  data=[]
  for e in x:
    d=go.Scatter(
      x=e['x'],
      y=e['y'],
      name=e[0],
      mode='markers',
      marker=dict(size=4))
    data.append(d)
  layout=go.Layout(title="Scatterplot prove", hovermode='closest', showlegend=True, xaxis_title=values[0], yaxis_title=values[1])
  fig=go.Figure(data=data, layout=layout)
  return fig

if __name__=='__main__':
  pand_sensores()
