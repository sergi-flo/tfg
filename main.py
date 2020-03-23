#!/usr/bin/env python3

import ppanda, graphs

def main():
 dic=ppanda.pand_sensores()
 x,y=graphs.dic_to_data(dic)
 graphs.graphic(x,y)


if __name__=='__main__':
  main()
