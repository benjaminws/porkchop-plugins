import os
import time

from porkchop.plugin import PorkchopPlugin

def sub(a, b, inter):
  jiffy = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

  return (float(b) - float(a)) / inter * 100 / jiffy

def read_info():
  data = {}

  f = open('/proc/stat', 'r')

  for line in f:
    if line.startswith('cpu'):
      fields = line.split()
      data[fields[0]] = fields[1:]
    else:
      break

  f.close()
  return data

class CpuPlugin(PorkchopPlugin):
  def get_data(self):
    data = {}

    fields = [
      'user',
      'nice',
      'system',
      'idle',
      'iowait',
      'irq',
      'softirq'
    ]

    hz = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

    if not self.__class__._cache:
      prev = read_info()
      delta = 1
      time.sleep(delta)
    else:
      prev = self.__class__._cache
      delta = time.time() - self.__class__._lastrefresh

    self.__class__._cache = cur = read_info()

    for key in cur.keys():
      data.setdefault(key, {})
      for pos in xrange(len(fields)):
        fname = fields[pos]
        data[key].update({
          fname: sub(prev[key][pos], cur[key][pos], delta)
        })

    return data