#!/usr/bin/env python3

import ppanda, graphs

def main():
 dic=ppanda.pand_sensores()
 x,y=graphs.dic_to_data(dic)
 graphs.graphic(x,y)


def main2():
  dic,dic_out=ppanda.pand_sensors()
  graphs.multiplot(dic,dic_out)

if __name__=='__main__':
  a=input('1-main(), 2-main2() --> ')
  if a=='1':
    main()
  elif a=='2':
    main2()
