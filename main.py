#!/bin/python3

###
### Parses a terraform plan raw to capture keyword. 
### Usage: python main.py <KEYWORD> <FILE>
### This reformats to add the command to each destroy and strip off the weird encoding on windows.
###

import os
import sys

tf_action_parse = '[1m  #' # present at beginning of <resource> will be destroyed
destroy_parse = '[0m will be [1m[31mdestroyed[0m' # present at the end of <resource> will be destroyed. Used to differentiate between destroy and other actions
create_parse = '[0m will be created'#' will be created'
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

def main():
    args = sys.argv
    if 2 > len(args):
        print("No keyword found. Keywords: created, destroyed")
        quit()
    if 3 > len(args):
        print("No plan file specified. Please add plan file after `python main.py <KEYWORD> <plan_file_name>`")
        quit()

    keyword_command = args[1]
    print(keyword_command)

    plan_file = args[2]
    print("plan file: ", plan_file)
    tf_plan_file = open(plan_file, 'r')
    lines = tf_plan_file.readlines()

    if keyword_command == "destroyed":
        destroys = destroy_commands(lines)
        print("destroy commands:\n{}".format("\n".join(destroys)))
    elif keyword_command == "created":
        creates = create_commands(lines)
        print("import commands:\n{}".format("\n".join(creates)))
        print("REMEMBER to add the required resouce ID for importing in the ending double quotes.")


if __name__ == "__main__":
    main()