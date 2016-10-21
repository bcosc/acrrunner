#!/usr/bin/env python

from __future__ import division
import sys
import arvados
import subprocess
import os
import math

# Taken from http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def main(args):
  wf_uuid = args[0]
  keep_mount = args[1]
  wf = arvados.api('v1').pipeline_instances().list(filters=[["uuid","=",wf_uuid]]).execute()
  job_uuids = []
  job_dict = {}
  job_list = wf['items'][0]['components'].keys()
  job_list.sort()
  out_path = os.path.join('/home/bcosc/output-colls', wf_uuid+'-outputsizes.txt')
  with open(out_path,'w') as out:
    out.write("job_name, file_name, filesize\n")
    for job_name in job_list:
      job_dict[job_name] = []
      job_uuid = wf['items'][0]['components'][job_name]['job']['uuid']
      job = arvados.api('v1').jobs().list(filters=[["uuid","=",job_uuid]]).execute()
      output_pdh = job['items'][0]['output']
      collection = arvados.collection.CollectionReader(output_pdh)
      for file in collection:
        stat = os.stat(os.path.join(keep_mount, output_pdh, file))
        filesize = stat.st_size
        out.write("%s, %s, %s\n" % (job_name, file, sizeof_fmt(filesize)))
  return out_path

if __name__ == '__main__':
  print main(sys.argv[1:])
