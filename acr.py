#!/usr/bin/env python

import sys
import argparse
import subprocess
import arvados
import time
import os

def parse_arguments(arglist):
  parser = argparse.ArgumentParser()
  parser.add_argument('workflow',
                      help="Input .cwl Workflow or CommandLineTool file")
  parser.add_argument('yaml',
                      help="Input .yml/.json document")
  parser.add_argument('--dry-run', '-n', action='store_true',
                      help="Don't create Arvados objects, log what would happen")
  parser.add_argument('--project_uuid', default='e51c5-j7d0g-2atyp0y6yoanxl6', 
                      help="Project UUID to store pipeline instance")
  args = parser.parse_args(arglist)
  return args

def main(arglist):
  args = parse_arguments(arglist)
  run_args = ['arvados-cwl-runner', '--local', '--verbose', 
              '--project-uuid', args.project_uuid,
              '--output-name', os.path.basename(args.yaml),
              args.workflow, args.yaml]
  with open('/tmp/acr.log','w') as acrlog:
    subprocess.check_call(run_args, stderr=acrlog)

  with open('/tmp/acr.log','r') as acrlog:
    instance_uuid = ''
    for line in acrlog:
      if not instance_uuid:
        if 'd1hrv' in line:
          instance_uuid = line.split(' ')[-1]
  arvados.api('v1').pipeline_instances().update(uuid=instance_uuid.strip(), body={'name' : args.yaml}).execute()
  return instance_uuid.strip()

if __name__ == '__main__':
  print main(sys.argv[1:])
#  try:
#    sys.stdout.write(main(sys.argv[1:]))
#  except:
#    sys.exit(main(sys.argv[1:]))
