#!/usr/bin/env python3

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.io import loadmat

file_path='dash/data_csv/HFOs_clean.csv'
brains_path ='dash/brains/brain'
positions_path ='dash/brains/positions'

def load_csv():
  d=pd.read_csv(file_path)
  labels=[i for i in d]
  return d[labels[1:]]

def needles_list(patient=None):
  d=load_csv()
  if patient!=None:
    d=d.loc[d['Patient']==patient]
  res=[]
  for e in d['Channel']:
    ee=''.join(filter(str.isalpha, e))
    if ee not in res:
      res.append(ee)
  return res

def patients():
  d=load_csv()
  patients_list=[]
  for patient in d['Patient']:
    if patient not in patients_list:
      patients_list.append(patient)
  return patients_list

def multiplot_data(selected_patient, selector, args):
  d=load_csv()
  filtered_d=d.loc[d['Patient']==selected_patient]
  needles=needles_list(selected_patient)
  a=[]
  res=[]
  if selector != 'needles':
    for e in d[selector]:
      if e not in a:
          d={0:e}
          for h in args:
            d[h]=[]
          res.append(d)
          a.append(e)
  else:
    for e in needles:
      d={0:e}
      for h in args:
        d[h]=[]
      res.append(d)
  for y in args:
    for e in res:
      if selector != 'needles':
        for row_selector, row_e in zip(filtered_d[selector], filtered_d[y]):
          if row_selector == e[0]:
            e[y].append(row_e)
      else:
        for row_selector, row_e in zip(filtered_d['Channel'], filtered_d[y]):
          if e[0]==''.join(filter(str.isalpha, row_selector)):
            e[y].append(row_e)
  return res

def multiplot(selected_patient, selector, values):
  x=multiplot_data(selected_patient, selector, values)
  data=[]
  for e in x:
    d=go.Splom(
    dimensions=[dict(label=k,values=e[k]) for k in e if k != 0],
    name=e[0],
    marker=dict(size=4),
    diagonal=dict(visible=False))
    data.append(d)
  layout=go.Layout(title="Multiplot", dragmode='select', hovermode='closest', showlegend=True)
  fig=go.Figure(data=data,layout=layout)
  return fig

def scatter_data(selected_patient, selector, args): #args=[x,y]
  d=load_csv()
  filtered_d=d.loc[d['Patient']==selected_patient]
  needles=needles_list(selected_patient)
  a=[]
  res=[]
  if selector != 'needles':
    for e in d[selector]:
        if e not in a:
            res.append({0:e, 'x':[], 'y':[]})
            a.append(e)
  else:
    for e in needles:
      res.append({0:e, 'x':[], 'y':[]})
  for e in res:
    if selector != 'needles':
      for row_selector, row_x, row_y in zip(filtered_d[selector], filtered_d[args[0]], filtered_d[args[1]]):
        if row_selector == e[0]:
          e['x'].append(row_x)
          e['y'].append(row_y)
    else:
      for row_selector, row_x, row_y in zip(filtered_d['Channel'], filtered_d[args[0]], filtered_d[args[1]]):
        if e[0]==''.join(filter(str.isalpha, row_selector)):
          e['x'].append(row_x)
          e['y'].append(row_y)
  return res

def scatter(selected_patient, selector, values):
  x=scatter_data(selected_patient, selector, values)
  data=[]
  for e in x:
    d=go.Scatter(
      x=e['x'],
      y=e['y'],
      name=e[0],
      mode='markers',
      marker=dict(size=4))
    data.append(d)
  layout=go.Layout(title="Scatterplot", hovermode='closest', showlegend=True, xaxis_title=values[0], yaxis_title=values[1])
  fig=go.Figure(data=data, layout=layout)
  return fig

def histogram_data(selected_patient, selector, args): #args=[x,y]
  d=load_csv()
  filtered_d=d.loc[d['Patient']==selected_patient]
  needles=needles_list(selected_patient)
  a=[]
  res=[]
  if selector != 'needles':
    for e in d[selector]:
        if e not in a:
            res.append({0:e, 'd':[], 'len':0})
            a.append(e)
  else:
    for e in needles:
      res.append({0:e, 'd':[], 'len':0})
  for e in res:
    if selector != 'needles':
      for row_selector, row_e in zip(filtered_d[selector], filtered_d[args]):
        if row_selector == e[0]:
          e['d'].append(row_e)
    else:
      for row_selector, row_e in zip(filtered_d['Channel'], filtered_d[args]):
        if e[0]==''.join(filter(str.isalpha, row_selector)):
          e['d'].append(row_e)
  for e in res:
    e['len']=len(e['d'])
  res.sort(key= lambda i: i['len'], reverse=True)
  return res

def histogram(selected_patient, selector, value):
  x=histogram_data(selected_patient, selector, value)
  data=[]
  for e in x:
    d=go.Histogram(
      x=e['d'],
      name=e[0],
      opacity=0.75,
      bingroup=1)
    data.append(d)
  layout=go.Layout(title_text="Histogram", showlegend=True, xaxis_title_text=value, yaxis_title_text='Count', barmode='overlay')
  fig=go.Figure(data=data, layout=layout)
  return fig

def heatmap():
  mat = loadmat('excel/data.mat')
  mat_data = mat['stockwell']
  data=go.Heatmap(
    z=mat_data
  )
  layout=go.Layout(title_text="Heatmap", showlegend=True, xaxis_title_text='X-axis', yaxis_title_text='Y-axis')
  fig=go.Figure(data=data, layout=layout)
  return fig

def scatter3d_data(selected_patient, selector, args): #args=[x,y,z]
  d=load_csv()
  filtered_d=d.loc[d['Patient']==selected_patient]
  needles=needles_list(selected_patient)
  a=[]
  res=[]
  if selector != 'needles':
    for e in d[selector]:
        if e not in a:
            res.append({0:e, 'x':[], 'y':[], 'z':[]})
            a.append(e)
  else:
    for e in needles:
      res.append({0:e, 'x':[], 'y':[], 'z':[]})
  for e in res:
    if selector != 'needles':
      for row_selector, row_x, row_y, row_z in zip(filtered_d[selector], filtered_d[args[0]], filtered_d[args[1]], filtered_d[args[2]]):
        if row_selector == e[0]:
          e['x'].append(row_x)
          e['y'].append(row_y)
          e['z'].append(row_z)
    else:
      for row_selector, row_x, row_y, row_z in zip(filtered_d['Channel'], filtered_d[args[0]], filtered_d[args[1]], filtered_d[args[2]]):
        if e[0]==''.join(filter(str.isalpha, row_selector)):
          e['x'].append(row_x)
          e['y'].append(row_y)
          e['z'].append(row_z)
  return res

def scatter3d(selected_patient, selector, values):
  x=scatter3d_data(selected_patient, selector, values)
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
  layout=go.Layout(title="3D Scatterplot", hovermode='closest', showlegend=True, scene=dict(xaxis_title=values[0], yaxis_title=values[1], zaxis_title=values[2]))
  fig=go.Figure(data=data, layout=layout)
  return fig

def list_needles_3dscatter(filtered_d, needles):
  res=[]
  for e in needles:
    dic={0:e, 'data':[]}
    a=[]
    for y, row_x, row_y, row_z in zip(filtered_d['Channel'], filtered_d['x'], filtered_d['y'], filtered_d['z']):
      if (e==''.join(filter(str.isalpha, y))) and (y not in a):
        dic['data'].append({0:y, 'xyz':[row_x, row_y, row_z], 'd':[], 'd_scale':[]})
        a.append(y)
    res.append(dic)
  return res

def scatter3d_needles_data(selected_patient, args):
  d=load_csv()
  filtered_d=d.loc[d['Patient']==selected_patient]
  res=list_needles_3dscatter(filtered_d, needles_list(selected_patient))
  for e in res:
    for y in e['data']:
      for row_selector, value in zip(filtered_d['Channel'], filtered_d[args]):
        if y[0]==row_selector:
          y['d'].append(value)
  mini=0
  maxi=0
  for e in res:
    for y in e['data']:
      calc=sum(y['d'])/len(y['d'])
      y['d']=calc
      if calc>maxi:
        maxi=calc
      if calc<mini:
        mini=calc
  scale_factor=maxi-mini
  for e in res:
    for y in e['data']:
      scale=(y['d']/scale_factor)*25
      y['d_scale']=scale
  return res

def scatter3d_needles(selected_patient, values, show_brain, brain_opacity):
  brain = loadmat(brains_path+selected_patient+'.mat', squeeze_me=True)
  data=[]
  x=scatter3d_needles_data(selected_patient, values)
  for e in x:
    d=go.Scatter3d(
      x=[k['xyz'][0] for k in e['data']],
      y=[k['xyz'][1] for k in e['data']],
      z=[k['xyz'][2] for k in e['data']],
      name=e[0],
      mode='markers',
      text=[k[0] for k in e['data']],
      customdata=[[k['d'], values] for k in e['data']],
      hovertemplate=
      "<b>%{text}</b><br>" +
      "%{customdata[1]} = %{customdata[0]:.02f}<br>" +
      "<extra></extra>",
      marker = dict(
        sizemode='diameter',
        sizeref=1,
        size=[k['d_scale'] for k in e['data']],
      ),
      )
    data.append(d)
  if show_brain==[1]:
    data.append(go.Mesh3d(
        # 8 vertices of a cube
        x=[a[0] for a in brain['Vertices']],
        y=[a[1] for a in brain['Vertices']],
        z=[a[2] for a in brain['Vertices']],
        opacity=brain_opacity/100,
        # i, j and k give the vertices of triangles
        i=[a[0]-1 for a in brain['Faces']],
        j=[a[1]-1 for a in brain['Faces']],
        k=[a[2]-1 for a in brain['Faces']],
        name='y',
        color='grey',
    ))
  layout=go.Layout(title="3D Scatterplot needles", hovermode='closest', showlegend=True, scene=dict(xaxis_title='X-axis', yaxis_title='Y-axis', zaxis_title='Z-axis'))
  fig=go.Figure(data=data, layout=layout)
  return fig

def colored_dic(selected_patient, values):
  x=scatter3d_needles_data(selected_patient, values)
  data={'needle_group':[], 'x':[], 'y':[], 'z':[], 'text':[], 'color':[]}
  for e in x:
    for y in e['data']:
      data['x'].append(y['xyz'][0])
      data['y'].append(y['xyz'][1])
      data['z'].append(y['xyz'][2])
      data['text'].append(y[0])
      data['color'].append(y['d'])
  return data

def scatter3d_color_needles(selected_patient, values, show_brain, brain_opacity):
  colored_data=colored_dic(selected_patient, values)
  brain = loadmat(brains_path+selected_patient+'.mat', squeeze_me=True)
  d=[go.Scatter3d(
    x=[k for k in colored_data['x']],
    y=[k for k in colored_data['y']],
    z=[k for k in colored_data['z']],
    #name=e[0],
    mode='markers',
    text=[k for k in colored_data['text']],
    customdata=[[k, values] for k in colored_data['color']],
    hovertemplate=
    "<b>%{text}</b><br>" +
    "%{customdata[1]} = %{customdata[0]:.02f}<br>" +
    "<extra></extra>",
    marker = dict(
      sizemode='diameter',
      sizeref=1,
      color=[k for k in colored_data['color']],
      colorbar=dict(thickness=20),
    ),
    )]
  if show_brain==[1]:
    d.append(go.Mesh3d(
        # 8 vertices of a cube
        x=[a[0] for a in brain['Vertices']],
        y=[a[1] for a in brain['Vertices']],
        z=[a[2] for a in brain['Vertices']],
        opacity=brain_opacity/100,
        # i, j and k give the vertices of triangles
        i=[a[0]-1 for a in brain['Faces']],
        j=[a[1]-1 for a in brain['Faces']],
        k=[a[2]-1 for a in brain['Faces']],
        name='y',
        color= 'grey',
    ))
  layout=go.Layout(title="3D Scatterplot needles colored", hovermode='closest', scene=dict(xaxis_title='X-axis', yaxis_title='Y-axis', zaxis_title='Z-axis'))
  fig=go.Figure(data=d, layout=layout)
  return fig


if __name__=='__main__':
  pass


'''
def dic_to_data(d):
  x=[]
  y=[]
  for sensor in d:
    x.append(sensor)
    median=sum([float(e) for e in d[sensor]])/len(d[sensor])
    y.append(median)
  return x,y

def pand_sensores(selected_patient):
  dic={}
  d=load_csv()
  for amplitude, patient, channel in zip(d['Amplitude'],d['Patient'],d['Channel']):
    if selected_patient in patient:
      if channel in dic:
        dic[channel].append(amplitude)
      else:
        dic[channel] = [amplitude]
  #print(dic, len(dic))
  return dic

def multiplot_soz1(selected_patient, *args):
  d=load_csv()
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
'''
