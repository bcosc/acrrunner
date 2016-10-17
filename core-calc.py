#!/usr/bin/env python

import sys
import arvados

def main(args):
  wf_uuid = args[0]
  wf = arvados.api('v1').pipeline_instances().list(filters=[["uuid","=",wf_uuid]]).execute()
  job_uuids = []
  for job_name in wf['items'][0]['components']:
    job_uuids.append(wf['items'][0]['components'][job_name]['job']['uuid'])

if __name__ == '__main__':
  print main(sys.argv[1:])

