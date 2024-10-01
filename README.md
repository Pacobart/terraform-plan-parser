
# terraform-plan-parser

## Overview

This script will parse a terraform plan output and generate the commands needed to manipulate a state file. This is useful during migrations. 
The primary use case this solves for is splitting a terraform state into 2 without having to destroy the terraform resources and recreate.

### Terraform Cloud Usage

1. Run a plan on the workspace in terraform cloud and download the raw plan by pressing `View raw log`
2. Copy the plan and rename to the workspace name to avoid confusion. Ex: starting-plan-log.txt
3. Run `python main.py starting-plan-log.txt destroyed` to output the terraform state removal commands
4. Run the state removal commands against the workspace
5. Run another plan on the workspace in terraform cloud and validate for no `destroys` in the plan


### Jenkins usage
Download console output by clicking "View as plain text", right click and save as the webpage to a file.

### Commands
```
python main.py plan-log.txt destroyed
python main.py plan-log.txt created
python main.py plan-log.txt created --out hcl
python main.py plan-log.txt created --out cli
```

## Testing

```
python -m unittest tests/test_main.py
```
