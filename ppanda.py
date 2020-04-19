#!/usr/bin/env python3

import pandas as pd
import plotly.graph_objects as go
from scipy.io import loadmat

def load_panda():
  d=pd.read_csv('excel/hfos_final.csv')
  labels=[i for i in d]
  return d[labels[1:]]

def neddles_list():
  d=load_panda()
  res=[]
  for e in d['Channel']:
    ee=''.join(filter(str.isalpha, e))
    if ee not in res:
      res.append(ee)
  return res

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

def multiplot_soz1(selected_patient, *args):
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


def multiplot_soz(selected_patient, selector, args):
  d=load_panda()
  filtered_d=d.loc[d['Patient']==selected_patient]
  neddles=neddles_list()
  a=[]
  res=[]
  if selector != 'Neddles':
    for e in d[selector]:
      if e not in a:
          d={0:e}
          for h in args:
            d[h]=[]
          res.append(d)
          a.append(e)
  else:
    for e in neddles:
      d={0:e}
      for h in args:
        d[h]=[]
      res.append(d)
  for y in args:
    for e in res:
      if selector != 'Neddles':
        for row_selector, row_e in zip(filtered_d[selector], filtered_d[y]):
          if row_selector == e[0]:
            e[y].append(row_e)
      else:
        for row_selector, row_e in zip(filtered_d['Channel'], filtered_d[y]):
          if e[0] in row_selector:
            e[y].append(row_e)
  return res

def mp(selected_patient, selector, values):
  x=multiplot_soz(selected_patient, selector, values)
  data=[]
  for e in x:
    d=go.Splom(
    dimensions=[dict(label=k,values=e[k]) for k in e if k != 0],
    name=e[0],
    marker=dict(size=4),
    diagonal=dict(visible=False))
    data.append(d)
  layout=go.Layout(title="Multiplot prove", dragmode='select', hovermode='closest', showlegend=True)
  fig=go.Figure(data=data,layout=layout)
  return fig

def scatter_soz(selected_patient, selector, args): #args=[x,y]
  d=load_panda()
  filtered_d=d.loc[d['Patient']==selected_patient]
  neddles=neddles_list()
  a=[]
  res=[]
  if selector != 'Neddles':
    for e in d[selector]:
        if e not in a:
            res.append({0:e, 'x':[], 'y':[]})
            a.append(e)
  else:
    for e in neddles:
      res.append({0:e, 'x':[], 'y':[]})
  for e in res:
    if selector != 'Neddles':
      for row_selector, row_x, row_y in zip(filtered_d[selector], filtered_d[args[0]], filtered_d[args[1]]):
        if row_selector == e[0]:
          e['x'].append(row_x)
          e['y'].append(row_y)
    else:
      for row_selector, row_x, row_y in zip(filtered_d['Channel'], filtered_d[args[0]], filtered_d[args[1]]):
        if e[0] in row_selector:
          e['x'].append(row_x)
          e['y'].append(row_y)
  return res

def scatter(selected_patient, selector, values):
  x=scatter_soz(selected_patient, selector, values)
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

def histogram_soz(selected_patient, selector, args): #args=[x,y]
  d=load_panda()
  filtered_d=d.loc[d['Patient']==selected_patient]
  neddles=neddles_list()
  a=[]
  res=[]
  if selector != 'Neddles':
    for e in d[selector]:
        if e not in a:
            res.append({0:e, 'd':[], 'len':0})
            a.append(e)
  else:
    for e in neddles:
      res.append({0:e, 'd':[], 'len':0})
  for e in res:
    if selector != 'Neddles':
      for row_selector, row_e in zip(filtered_d[selector], filtered_d[args]):
        if row_selector == e[0]:
          e['d'].append(row_e)
    else:
      for row_selector, row_e in zip(filtered_d['Channel'], filtered_d[args]):
        if e[0] in row_selector:
          e['d'].append(row_e)
  for e in res:
    e['len']=len(e['d'])
  res.sort(key= lambda i: i['len'], reverse=True)
  return res

def histogram(selected_patient, selector, value):
  x=histogram_soz(selected_patient, selector, value)
  data=[]
  for e in x:
    d=go.Histogram(
      x=e['d'],
      name=e[0],
      opacity=0.75,
      bingroup=1)
    data.append(d)
  layout=go.Layout(title_text="Histogram prove", showlegend=True, xaxis_title_text=value, yaxis_title_text='Count', barmode='overlay')
  fig=go.Figure(data=data, layout=layout)
  return fig

def heatmap():
  mat = loadmat('excel/data.mat')
  mat_data = mat['stockwell']
  data=go.Heatmap(
    z=mat_data
  )
  layout=go.Layout(title_text="Heatmap prove", showlegend=True, xaxis_title_text='X-axis', yaxis_title_text='Y-axis')
  fig=go.Figure(data=data, layout=layout)
  return fig

def scatter3d_soz(selected_patient, selector, args): #args=[x,y,z]
  d=load_panda()
  filtered_d=d.loc[d['Patient']==selected_patient]
  neddles=neddles_list()
  a=[]
  res=[]
  if selector != 'Neddles':
    for e in d[selector]:
        if e not in a:
            res.append({0:e, 'x':[], 'y':[], 'z':[]})
            a.append(e)
  else:
    for e in neddles:
      res.append({0:e, 'x':[], 'y':[], 'z':[]})
  for e in res:
    if selector != 'Neddles':
      for row_selector, row_x, row_y, row_z in zip(filtered_d[selector], filtered_d[args[0]], filtered_d[args[1]], filtered_d[args[2]]):
        if row_selector == e[0]:
          e['x'].append(row_x)
          e['y'].append(row_y)
          e['z'].append(row_z)
    else:
      for row_selector, row_x, row_y, row_z in zip(filtered_d['Channel'], filtered_d[args[0]], filtered_d[args[1]], filtered_d[args[2]]):
        if e[0] in row_selector:
          e['x'].append(row_x)
          e['y'].append(row_y)
          e['z'].append(row_z)
  return res

def scatter3d(selected_patient, selector, values):
  x=scatter3d_soz(selected_patient, selector, values)
  data=[]
  for e in x:
    d=go.Scatter3d(
      x=e['x'],
      y=e['y'],
      z=e['z'],
      name=e[0],
      mode='markers',
      marker=dict(size=4))
    data.append(d)
  layout=go.Layout(title="3D Scatterplot prove", hovermode='closest', showlegend=True, scene=dict(xaxis_title=values[0], yaxis_title=values[1], zaxis_title=values[2]))
  fig=go.Figure(data=data, layout=layout)
  return fig

if __name__=='__main__':
  pand_sensores()
