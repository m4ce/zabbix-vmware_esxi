#!/usr/bin/env python
#
# vmware-esxi-cim.py
#
# VMware ESXi CIM monitoring plugin
#
# Author: Matteo Cerutti <matteo.cerutti@hotmail.co.uk>
#

import sys
import pywbem
import json
from setproctitle import setproctitle
from optparse import OptionParser

def cim_read_property(class_name, element_name, property_names = []):
  properties = {}

  class_data = client.GetClass(class_name, IncludeQualifiers=True)
  instance_list = client.EnumerateInstances(class_name)
  for instance in instance_list:
    if (
        ('ElementName' in instance and instance['ElementName'] == element_name) or
        ('Name' in instance and instance['Name'] == element_name) or
        ('Description' in instance and instance['Description'] == element_name)):


      if len(property_names) == 0:
        property_names = sorted(instance.keys())

      for property_name in property_names:
        if property_name in instance:
          if isinstance(instance[property_name], (list, tuple)):
            property_values = instance[property_name]
          else:
            property_values = [instance[property_name]]

          for value in property_values:
            if isinstance(value, (int, long, float, complex)):
              if value == False:
                val = 0
              elif value == True:
                val = 1
              else:
                val = value

              if property_name not in properties:
                properties[property_name] = val
              else:
                properties[property_name] = max(properties[property_name], val)
            elif isinstance(value, basestring):
              properties[property_name] = value
            elif value is None:
              if property_name == 'HealthState' or property_name == 'OperationalStatus':
                properties[property_name] = -1
              else:
                properties[property_name] = ''
            else:
              if property_name not in properties:
                properties[property_name] = []

              properties[property_name].append(value)

      break

  return properties

def main():
  parser = OptionParser(usage = 'Usage: %prog [options] <discovery|inspect [<property>]>')
  parser.add_option('-H', '--host', dest = 'host', help = 'VMware ESXi host')
  parser.add_option('-u', '--username', dest = 'username', help = 'VMware ESXi user')
  parser.add_option('-p', '--password', dest = 'password', help = 'VMware ESXi password')
  parser.add_option('--cim-classname', dest = 'cim_class_name', help = 'CIM class name')
  parser.add_option('--cim-elementname', dest = 'cim_element_name', help = 'CIM element name')
  parser.add_option('--cim-namespace', dest = 'cim_namespace', default = 'root/cimv2', help = 'CIM namespace')

  (options, args) = parser.parse_args()

  if not options.host:
    parser.error("VMWare ESXi host is required")

  if not options.username:
    parser.error("VMWare ESXi username is required")

  if not options.password:
    parser.error("VMWare ESXi password is required")

  if not options.cim_class_name:
    parser.error("CIM class name is required")

  if len(args) == 0:
    parser.error("Action is required")

  # remove password from command-line
  title = []
  for arg in sys.argv:
    str = arg
    if len(title) > 0:
      if title[-1] == '-p' or title[-1] == '--password':
        str = "xxxxx"

    title.append(str)

  setproctitle(' '.join(title))

  action = args[0]

  try:
    global client
    client = pywbem.WBEMConnection(options.host, (options.username, options.password), options.cim_namespace)

    if action == "discovery":
      obj = {}
      obj['data'] = []

      instance_list = client.EnumerateInstances(options.cim_class_name)

      for instance in instance_list:
        if 'ElementName' in instance:
          element_name = instance['ElementName']
        elif 'Name' in instance and instance['Name'] is not None and instance['Name'] != 'null':
          element_name = instance['Name']
        else:
          element_name = instance['Description']

        obj['data'].append({
          '{#ELEMENT_NAME}': element_name
        })

      print json.dumps(obj, indent = 4)
    elif action == "inspect":
      if not options.cim_element_name:
        parser.error("CIM element name is required")

      if len(args) >= 2:
        property_names = args[1:]
      else:
        property_names = []

      properties = cim_read_property(options.cim_class_name, options.cim_element_name, property_names)

      if len(properties) == 1:
        print properties.itervalues().next()
      else:
        for key, value in properties.iteritems():
          print "%s -> %s" % (key, value)
    else:
      parser.print_help()
      sys.exit(1)

  except Exception, e:
    sys.stderr.write("%s: caught exception (%s)\n" % (options.host, e))

if __name__ == "__main__":
  main()
