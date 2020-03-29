#!/usr/bin/env python3

import pandas as pd

def load_panda():
  d=pd.read_csv('excel/hfos.csv')
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


def pand_sensores():
  dic={}
  d=load_panda()
  for amplitude, patient, channel  in zip(d['Amplitude'],d['Patient'],d['Channel']):
    if 'PAT_1' in patient:
      if channel in dic:
        dic[channel].append(amplitude)
      else:
        dic[channel] = [amplitude]
  print(dic, len(dic))
  return dic

if __name__=='__main__':
  pand_sensores()
