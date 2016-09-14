#!/usr/bin/env python
import os
import uuid
import json
import argparse


def parse_args():
    my_parser = argparse.ArgumentParser()

    sub_parsers = my_parser.add_subparsers()

    create_configs_parser = sub_parsers.add_parser(
        "create-configs", conflict_handler='resolve')
    create_configs_parser.add_argument(
        "-n", "--num_runs", help="Number of runs to create configurations for.", dest="num_runs", required=False, type=int)
    create_configs_parser.add_argument(
        "-c", "--config_location", help="Path to a directory where the generated config files will be stored.", dest="config_location", required=True)
    create_configs_parser.add_argument(
        "-s", "--sample_location", help="Path to a directory where the sample files are stored.", dest="sample_location", required=True)
    
    create_configs_parser.set_defaults(func=create_configs_command)

    my_args = my_parser.parse_args()

    return my_args


contig_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
               "11", "12", "13", "14", "15", "16", "17", "18", "19", 
               "20", "21", "22", "X", "Y"]

def write_config_to_file(config, config_location):

    run_uuid = str(uuid.uuid4())

    my_file = open("{}/{}.json".format(config_location, run_uuid), "w")
    json.dump(config, my_file)
    my_file.close()


def create_configs_command(args):

    num_runs = args.num_runs
    config_location = args.config_location
    sample_location = args.sample_location
    
    num_configs = 0
    
    if (not os.path.isdir(config_location)):
        os.makedirs(config_location)

    postfix = ".vcf.gz_filtered.vcf.gz"
    postfixed_contig_list = map(lambda(x): x + postfix, contig_list)
    
    
    for root, dirs, files in os.walk(sample_location):
        sample_id = os.path.basename(root)
        
        filename_list = map(lambda(x): sample_id + "_" + x, postfixed_contig_list)
        
        if num_runs == None or num_configs < num_runs:
            this_config_data = {
                                "sample": {
                                           "sample_id": sample_id,
                                           "filename_list": filename_list
                                           }
                                }
            write_config_to_file(this_config_data, config_location)
            num_configs = num_configs + 1
        elif num_configs >= num_runs:
            return

    

if __name__ == '__main__':
    args = parse_args()
    args.func(args)
