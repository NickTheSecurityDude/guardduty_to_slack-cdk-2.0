########################################################################################
#
# events_stack.py
#
# Resources:
#  lambda_target - lambda function events rule will target
#  events.Rule - rule to watch for guardduty finding
#  add_target - adds the lambda target to the rule
#
# Imports:  XX - Does not exist in cdk yet use cr lambda
#  lambda_function - IFunction from lambda stack
#
########################################################################################

from aws_cdk import (
  aws_events as events,
  aws_iam as iam,
  aws_events_targets as targets,
  core
)

class EventsStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, lambda_function,  **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)


    # Add lambda target for event bridge
    lambda_target=targets.LambdaFunction(
      handler=lambda_function
    )

    # Add event bridge rule
    events_rule=events.Rule(self,"GuardDutyEBRule",
      description="GuardDuty EB Rule",
      rule_name="guardduty_to_slack_rule",
      event_pattern=events.EventPattern(
        source=["aws.guardduty"],
        detail_type=["GuardDuty Finding"]
      )
    )

    # Add target to bridge rule
    events_rule.add_target(lambda_target)

