#!/usr/bin/env python

import sys
import os
import shutil.copyfile

base_yml = sys.argv[1]
collection_uuid = sys.argv[2]
collection_json = arvados.api('v1').collections().list(filters=[["uuid","=", collection_uuid]]).execute()
collection_name_trunc = collection_json.items()[1][1][0]['name'].split(' ')[0]
dir_base_yml = os.path.dirname(os.path.realpath(base_yml))
new_yaml_path = os.path.join(dir_base_yml, collection_name_trunc)
shutil.copyfile(base_yml, new_yaml_path)

with open(new_yaml_path,'a') as out:
  out.write("bclinput:\n")
  out.write("  class: Directory\n")
  out.write("  path: keep:%s\n" % need_searchable_keep_path)
  out.write("bclcsv:\n"
  out.write("  class: File\n")
  out.write("  path: keep:%s\n" % need_searchable_keep_path)
  
