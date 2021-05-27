# Send GuardDuty Notices to Slack

<img src="https://securitydude-article-images.s3.amazonaws.com/guardduty2slack/guardduty-slack-27a.png" width="800">

1. Clone this repo

2. Create a channel called #guardduty

3. Enter your web hook in var.py

4. Bootstrap and Launch the project
```
cdk bootstrap aws://<ACCT_ID>/<REGION>
cdk deploy --all --require-approval never
```
<img src="https://securitydude-article-images.s3.amazonaws.com/guardduty2slack/gd2slk-27a-cli.png" width="800">

5. Spin up an EC2 instance and run the following command to generate a sample GuardDuty Alert:
```
dig GuardDutyC2ActivityB.com any
```
6. Wait up to about an hour for your message to appear (this is the normal time GuardDuty takes to report a finding)

- If you need to create a webhook see:
https://api.slack.com/messaging/webhooks
