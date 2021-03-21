"""Shim for calling SAM translator"""
#pylint: disable = line-too-long,import-error
import argparse
from ast import literal_eval
from typing import Dict
import sys

import yaml
from samtranslator.policy_template_processor.processor import PolicyTemplatesProcessor
import samtranslator.policy_template_processor.exceptions as translator_errors

# This is the set of policy templates that Amazon provides for serverless apps:
# https://github.com/aws/serverless-application-model/blob/develop/samtranslator/policy_templates_data/policy_templates.json
# Lucky for us, the class has a utility method to load and validate the JSON document.
aws_templates = PolicyTemplatesProcessor.get_default_policy_templates_json()
ptp = PolicyTemplatesProcessor(aws_templates)

def get_policy(policy_name : str, parameters: Dict[str, any]) -> Dict[str, any]:
    """
    Get a completed IAM policy statement from the named policy ready for inclusion in a CloudFormation template.

    Args:
        policy_name (str): The SAM policy template name
        parameters (Dict[str, any]): The policy arguments

    Returns:
        Dict[str, any]: An IAM policy statement.

    Raises:
        InsufficientParameterValues: If the parameter values do not have values for all required parameters
        TemplateNotFoundException: If the policy_name is not present in the set of SAM policy templates
    """
    return ptp.convert(policy_name, parameters)

def show_policy_names() -> None:
    """Dump SAM policy names to standard out, one per line"""
    for policy_name in ptp.policy_templates.keys():
        print(policy_name)

def main():
    parser = argparse.ArgumentParser(description='Expand SAM policy templates')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list", action="store_true", help="List policy names")
    group.add_argument("-e", "--expand", action="store_true")
    parser.add_argument('--policy_name', help='SAM policy template name')
    parser.add_argument('--policy_args', help='Arguments to pass to template', default='{}')

    args = parser.parse_args()
    if args.list:
        show_policy_names()
    else:
        template_params = {}
        if args.policy_args:
            template_params = literal_eval(args.policy_args)
        try:
            result = get_policy(args.policy_name, template_params)
            print(yaml.dump(result))
        except translator_errors.InsufficientParameterValues as missing_param:
            print(missing_param)
            sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
