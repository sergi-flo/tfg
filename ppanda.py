#!/usr/bin/env python3

import pandas as pd

def pand():
  out,noOut= 0,0
  data=pd.read_excel('hfos.xlsx')
  #print(data[data.columns[0]])
  #print(data)
  for e in data[data.columns[0]]:
    if 'Outside' in e:
      out +=1
    else:
      noOut +=1
  total=out+noOut
  print(out, noOut, total)


def pand_sensores():
  dic={}
  data=pd.read_excel('hfos.xlsx')
  for row in data[data.columns[0]]:
    list_row=row.split(',')
    if 'PAT_1' in  list_row:
      if list_row[-2] in dic:
        dic[list_row[-2]].append(list_row[17])
      else:
        dic[list_row[-2]]=[list_row[17]]
  #print(dic, len(dic))
  return dic
  

def pand_sensors():
  dic={'Amplitude':[],'Oscillations':[],'Inst freq':[]}
  dic_out={'Amplitude':[],'Oscillations':[],'Inst freq':[]}
  data=pd.read_excel('hfos.xlsx')
  for row in data[data.columns[0]]:
    list_row=row.split(',')
    if 'Outside' in  list_row:
      dic_out['Amplitude'].append(list_row[17])
      dic_out['Oscillations'].append(list_row[12])
      dic_out['Inst freq'].append(list_row[20])
    else:
      dic['Amplitude'].append(list_row[17])
      dic['Oscillations'].append(list_row[12])
      dic['Inst freq'].append(list_row[20])
  #print(len(dic), '\n\n', len(dic_out))
  return dic,dic_out

if __name__=='__main__':
  pand_sensors()
