#!/bin/python3

###
### Parses a terraform plan raw to capture keyword. 
### Usage: python main.py <KEYWORD> <FILE>
### This reformats to add the command to each destroy and strip off the weird encoding on windows.
###

import os
import sys
import argparse

#tf_action_parse = '[1m  #' # present at beginning of <resource> will be destroyed. tfc plan
tf_action_parse = '[1m  #' # present at beginning of <resource> will be destroyed. gitlab plan
#destroy_parse = '[0m will be [1m[31mdestroyed[0m' # present at the end of <resource> will be destroyed. Used to differentiate between destroy and other actions. tfc
destroy_parse = '[0m will be [1m[31mdestroyed[0m' # present at the end of <resource> will be destroyed. Used to differentiate between destroy and other actions. gitlab
#create_parse = '[0m will be created'#' will be created'. tfc
create_parse = '[0m will be created'#' will be created'. gitlab
tf_rm_command = 'terraform state rm -ignore-remote-version' # command to prepend to each destroy line
tf_create_command = 'terraform import -ignore-remote-version'

def line_cleanup(input):
    input = input.replace(destroy_parse, '')
    input = input.replace(create_parse, '')
    input = input.replace('{} '.format(tf_action_parse), '')
    input = input.replace('"', r'\"')
    return input

def destroy_commands(lines):
    destroys = []
    count = 0
    for line in lines:
        line = line.strip() # remove newline
        if line.startswith(tf_action_parse):
            count += 1
            if destroy_parse in line:
                line = line_cleanup(line)
                line = "{} \"{}\"".format(tf_rm_command, line)
                destroys.append(line)
    return destroys

def create_commands(lines):
    creates = []
    count = 0
    for line in lines:
        line = line.strip()
        if line.startswith(tf_action_parse):
            count += 1
            if create_parse in line:
                line = line_cleanup(line)
                line = "{} \"{}\" \"\"".format(tf_create_command, line)
                creates.append(line)
    return creates

def destroy_hcl(lines):
    destroys = []
    count = 0
    for line in lines:
        line = line.strip() # remove newline
        if line.startswith(tf_action_parse):
            count += 1
            if destroy_parse in line:
                line = line_cleanup(line)
                line = format_hcl("destroyed", line)
                destroys.append(line)
    return destroys

def create_hcl(lines):
    creates = []
    count = 0
    for line in lines:
        line = line.strip()
        if line.startswith(tf_action_parse):
            count += 1
            if create_parse in line:
                line = line_cleanup(line)
                line = format_hcl("created", line)
                creates.append(line)
    return creates

def format_hcl(keyword, line):
    hcl_from = ''
    hcl_to = ''
    if keyword == 'created':
        hcl_to = line
    if keyword == 'destroyed':
        hcl_from = line
    hcl = f'moved {{\n  from = {hcl_from}\n  to = {hcl_to}\n}}'
    return hcl

def main():
    parser = argparse.ArgumentParser(
        prog='TerraformPlanParser',
        description='Parse Terraform Plans for create/destroys to output commands'
    )
    parser.add_argument('filename', help='python3 main.py myfile.txt')
    parser.add_argument('keyword', choices=['created', 'destroyed'], help='python3 main.py myfile.txt created|destroyed')
    parser.add_argument('-o', '--out', choices=['cli', 'hcl'], default='cli', type=str)
    args = parser.parse_args()

    output_command = args.out

    keyword_command = args.keyword
    print(keyword_command)

    plan_file = args.filename
    print("plan file: ", plan_file)
    tf_plan_file = open(plan_file, 'r')
    lines = tf_plan_file.readlines()

    if keyword_command == "destroyed":
        if output_command == "cli":
            destroys = destroy_commands(lines)
        elif output_command == "hcl":
            destroys = destroy_hcl(lines)
        print("destroy commands:\n{}".format("\n".join(destroys)))
    elif keyword_command == "created":
        if output_command == "cli":
            creates = create_commands(lines)
        elif output_command == "hcl":
            creates = create_hcl(lines)
        print("import commands:\n{}".format("\n".join(creates)))
        print("REMEMBER to add the required resouce ID for importing in the ending double quotes.")


if __name__ == "__main__":
    main()