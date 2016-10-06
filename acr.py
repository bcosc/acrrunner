#!/usr/bin/env python

import sys
import argparse

def parse_arguments(arglist):
  parser = argparse.ArgumentParser()
  parser.add_argument('--workflow', '-W', metavar='CWLDOCUMENT',
                      help="Input .cwl Workflow or CommandLineTool file")
  parser.add_argument('--yaml', '-Y', metavar='YAMLINPUT',
                      help="Input .yml/.json document")
  parser.add_argument('--dry-run', '-n', action='store_true',
                      help="Don't create Arvados objects, log what would happen")
  parser.add_argument('--project_uuid', default='e51c5-j7d0g-2atyp0y6yoanxl6', 
                      help="Don't create Arvados objects, log what would happen")
  args = parser.parse_args(arglist)
  return args

def main(arglist):
  args = parse_arguments(arglist)
  run_args = ['arvados-cwl-runner', '--local', '--verbose', 
              '--project_uuid', args.project_uuid,
              args.workflow, args.yaml]
  return run_args
  

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
