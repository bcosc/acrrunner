#!/usr/bin/env python

from __future__ import division
import sys
import arvados
import datetime
import feed.date.rfc3339
from decimal import Decimal

def node_round(min_cores_per_node):
  node_possibilities = [1,2,4,8,16,20]
  if min_cores_per_node in node_possibilities:
    return min_cores_per_node
  else:
    if min_cores_per_node < 4:
      return 4
    elif min_cores_per_node < 8:
      return 8
    elif min_cores_per_node < 16:
      return 16
    elif min_cores_per_node < 20:
      return 20

def RFC3339Convert_to_dt(rfc_time):
  default_time_offset = "EST"
  feed.date.rfc3339.set_default_time_offset(default_time_offset)
  timefloat = feed.date.rfc3339.tf_from_timestamp(rfc_time)
  timestamp = feed.date.rfc3339.timestamp_from_tf(timefloat)
  dt = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S' + default_time_offset)
  return dt

def Time_diff(early, late):
  diff = late - early
  diff_chop_ms = diff - datetime.timedelta(microseconds=diff.microseconds)
  return diff_chop_ms

def main(args):
  wf_uuid = args[0]
  wf = arvados.api('v1').pipeline_instances().list(filters=[["uuid","=",wf_uuid]]).execute()
  job_uuids = []
  job_dict = {}
  coretime = 0
  for job_name in wf['items'][0]['components']:
    job_dict[job_name] = []
    job_uuid = wf['items'][0]['components'][job_name]['job']['uuid']
    job = arvados.api('v1').jobs().list(filters=[["uuid","=",job_uuid]]).execute()
    job_time = Time_diff(RFC3339Convert_to_dt(job["items"][0]["started_at"]),RFC3339Convert_to_dt(job["items"][0]["finished_at"]))
    (h, m, s) = str(job_time).split(':')
    node_time = int(h) + int(m)/60 + int(s)/3600
    min_cores = job["items"][0]["runtime_constraints"]["min_cores_per_node"]
    cores = node_round(min_cores)
    job_coretime = cores*node_time
    coretime += job_coretime
    job_dict[job_name].append('%.3f' % job_coretime)
  return coretime, job_dict


if __name__ == '__main__':
  (c,j) = main(sys.argv[1:])
  print c
  print j
