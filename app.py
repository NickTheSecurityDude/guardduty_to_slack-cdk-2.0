#!/usr/bin/env python3

from aws_cdk import core

import boto3
import sys

import vars

client = boto3.client('sts')

region=client.meta.region_name

#if region != 'us-east-1':
#  print("This app may only be run from us-east-1")
#  sys.exit()

account_id = client.get_caller_identity()["Account"]

my_env = {'region': region, 'account': account_id}

from stacks.lambda_stack import LambdaStack
from stacks.events_stack import EventsStack

proj_name="gd2slack"

app = core.App()

lambda_stack=LambdaStack(app, proj_name+"-lambda",vars.project_vars['slack_webhook_url'],env=my_env)
events_stack=EventsStack(app, proj_name+"-events",lambda_stack.guardduty_to_slack_func)

app.synth()

# Tag all resources
for stack in [lambda_stack,events_stack]:
  core.Tags.of(stack).add("Project", proj_name)
  #core.Tags.of(stack).add("ProjectGroup", vars.project_vars['group_proj_name'])
