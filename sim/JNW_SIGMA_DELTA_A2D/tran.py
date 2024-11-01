#!/usr/bin/env python3
import pandas as pd
import yaml
import ltspice as lt
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math
import sys

def main(name):
  # Delete next line if you want to use python post processing
  # return
  yamlfile = name + ".yaml"

  sys.stdout.write("Reading YAML file: " + yamlfile + "\n")
  # Read result yaml file
  with open(yamlfile) as fi:
    obj = yaml.safe_load(fi)
  sys.stdout.write("Done reading YAML file: " + yamlfile + "\n")

  # Read raw file
  rawfile = name + ".raw"

  sys.stdout.write("Reading RAW file: " + rawfile + "\n")

  rawdata = lt.Ltspice(rawfile)

  rawdata.parse()

  time = rawdata.get_time()
  vq = rawdata.get_data('V(xdut.q)')
  vqn = rawdata.get_data('V(xdut.qn)')
  vres = rawdata.get_data('V(xdut.res)')
  vresb = rawdata.get_data('V(xdut.resb)')
  vcmp = rawdata.get_data('V(xdut.vcmp)')
  p1 = rawdata.get_data('V(xdut.p1)')
  p2 = rawdata.get_data('V(xdut.p2)')
  vo1 = rawdata.get_data('V(xdut.vo1)')
  vo2 = rawdata.get_data('V(xdut.vo2)')
  sys.stdout.write("Done reading RAW file: " + rawfile + "\n")

  # Do something to parameters
  vmid = 0.9
  vin = vmid+7e-3
  vfs = 0.5
  per = 1/16e6
  tstart = 1.5*per
  N = 64
  dout = vq
  t = time
  ts = np.arange(tstart, tstart+N*per, per)
  interp_func = interp1d(t, dout)
  dsamp = interp_func(ts)
  dsamp[dsamp > 0.9] = 1
  dsamp[dsamp < 0.9] = 0
  csum = np.cumsum(dsamp)
  out = vmid-vfs/2 + np.cumsum(csum)*2.0/N/(N+1)*vfs

  obj['ts'] = ts.tolist()
  obj['out'] = out.tolist()

  sys.stdout.write("Write YAML file: " + yamlfile + "\n")
  # Save new yaml file
  with open(yamlfile,"w") as fo:
    yaml.dump(obj,fo)

  sys.stdout.write("Done writing YAML file: " + yamlfile + "\n")
