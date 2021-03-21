# SAM IAM

> I do not like them,
> Sam-I-am
> I do not like
> [least privilege policies]
> - Dr. Seuss

## Background
One of the challenges with writing least privilege IAM policies is that it's tedious.  If you're an administrator or other super-user, things just work for you but not your users.
If you're a developer with a limited role, writing documents is a trial and error process.  Amazon recognized that when they created [SAM](https://github.com/aws/serverless-application-model).

SAM includes a number of [ready-made policies](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-template-list.html).  These policy templates distill the requirements for associated operations into a single call.  The resulting policy statement only includes the IAM actions and resources required. 

Unfortunately, it's not possible to use these policies directly in CloudFormation except as part of a serverless application.  If you're writing least privilege policies for EC2-based applications, you're out of luck.  Until now.

## Project Goals
The purpose of this project is two-fold.  First, it's an easy to understand example of how to integrate the SAM library into your own application.  Second, it provides a commandline shim that
allows you to dump the results of the template expansion as YAML to standard output.  The Amazon docs have the policies as JSON, but if you're writing CloudFormation as YAML it can be annoying to have to switch between the two.

In theory, the same JSON schema could be used to write your own policies.

```json
{
    "Version": "0.0.1",
    "Templates": {
        "MyPolicyTemplateName": {
            "Description": "What does this policy do?",
            "Parameters": "What parameters are required?",
            "Definition": {
                "Statement": []
            }
        }
    }
}
```

## Integration Help
The file [policy.py](./sam_iam/policy.py) shows how to create a template processor that includes the default SAM template policies.  The associated test cases include happy path cases for
both a hard-coded value and a value that comes from an intrinsic within the template.

## Commandline Execution
The package can also be executed at the command line.

```bash
expand-sam-policy -h
usage: expand-sam-policy [-h] [-l | -e] [--policy_name POLICY_NAME] [--policy_args POLICY_ARGS]

Expand SAM policy templates

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List policy names
  -e, --expand
  --policy_name POLICY_NAME
                        SAM policy template name
  --policy_args POLICY_ARGS
                        Arguments to pass to template
```
If the policy requires arguments, they need to be passed as a stringified Python dictionary:

```bash
expand-sam-policy --policy_name SQSPollerPolicy --policy_args '{"QueueName":"MyFirstQueue"}'
Statement:
- Action:
  - sqs:ChangeMessageVisibility
  - sqs:ChangeMessageVisibilityBatch
  - sqs:DeleteMessage
  - sqs:DeleteMessageBatch
  - sqs:GetQueueAttributes
  - sqs:ReceiveMessage
  Effect: Allow
  Resource:
    Fn::Sub:
    - arn:${AWS::Partition}:sqs:${AWS::Region}:${AWS::AccountId}:${queueName}
    - queueName: MyFirstQueue
```

Similarly, if this statement is granting access to a resource within the same CloudFormation template:

```bash
expand-sam-policy --policy_name SQSPollerPolicy --policy_args '{"QueueName": {"Fn::GetAtt": ["MyFirstQueue","QueueName"]}}'
Statement:
- Action:
  - sqs:ChangeMessageVisibility
  - sqs:ChangeMessageVisibilityBatch
  - sqs:DeleteMessage
  - sqs:DeleteMessageBatch
  - sqs:GetQueueAttributes
  - sqs:ReceiveMessage
  Effect: Allow
  Resource:
    Fn::Sub:
    - arn:${AWS::Partition}:sqs:${AWS::Region}:${AWS::AccountId}:${queueName}
    - queueName:
        Fn::GetAtt:
        - MyFirstQueue
        - QueueName
```