import os
import sys
import logging 
from os.path import expanduser as ex

logging.basicConfig(level=logging.DEBUG, format='%(name)s:: %(message)s')
LOG = logging.getLogger(__name__)


def line_is_ok(raw_line):
    return len(raw_line.split(";"))

def data_from_line(raw_line):
    return [ el.strip() for el in raw_line.split(";") ]

def open_mapping(mapping_path):
    if not os.path.exists(mapping_path):
         LOG.error("path not exists '{}'".format(mapping_path)) 
    with open(mapping_path, "r") as mapping:
         return ( data_from_line(line) for line in mapping.readlines() if line_is_ok(line) )


def deploy_confgs():
   mappings = open_mapping("mapping.txt") 
   if not mappings:
       LOG.error("Mapping is empty")
   
   for mapping in mappings:
       LOG.info("Mapping for {}; file from {} to {}".format(*mapping))
       mapping[2] = mapping[2].replace("~", ex("~"))

       if not os.path.exists(mapping[2]):
           LOG.info("Path not exists {}".format(os.path.dirname(mapping[2])))
           os.makedirs(os.path.dirname(mapping[2])) 

       if os.path.exists(os.path.abspath(mapping[2])):
           LOG.info("Path exists {0} moving to {0}_back".format(mapping[2]))
           os.rename(os.path.abspath(mapping[2]), os.path.abspath(mapping[2])+"_back")

       os.symlink(os.path.abspath(mapping[1]), os.path.abspath(mapping[2]))
       LOG.info("Symbolic link created {}".format(os.path.abspath(mapping[2])))

if __name__ == "__main__":
    deploy_confgs()
   
