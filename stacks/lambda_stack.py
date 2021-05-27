#########################################################################
#
# lambda_stack.py
#
# Resources:
#  1 lambda functions (code in /lambda folder (from_asset))
#
# Exports:
#  guardduty_to_slack_func - IFunction to use in events bridge stack
#
########################################################################

from aws_cdk import (
  aws_iam as iam,
  aws_lambda as lambda_,
  core
)

class LambdaStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, slack_webhook_url, env, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # get acct id for policies
    #acct_id=env['account'] # not needed here

    # create the Lambda function
    self._guardduty_to_slack_func=lambda_.Function(self,"GuardDutyToSlackLambda",
      code=lambda_.Code.from_asset("lambda/"),
      handler="guardduty_to_slack.lambda_handler",
      runtime=lambda_.Runtime.PYTHON_3_8,
      #role=IRole, # lambda basic execution role is automagically created
      environment = {
          'URL': slack_webhook_url
      }
    )

  # Exports
  # Lambda IFunction to use in events bridge stack
  @property
  def guardduty_to_slack_func(self) -> lambda_.IFunction:
    return self._guardduty_to_slack_func

