#pylint: disable = line-too-long,no-self-use
"""
The system under test is a minimal shim around a utility package used by SAM.
The value of these test cases is therefore the alternative benefit of demonstrating *HOW* the system works.
"""
import pytest
import yaml # Enable debug output

from pprint import pprint # Enable debug output
from samtranslator.policy_template_processor.exceptions import TemplateNotFoundException
from sam_iam import policy


class TestPolicy:
    """Collection of tests showing how to use the wrapper"""
    def test_policy_lookup(self):
        """Confirm that policy lookup works"""
        result = policy.get_policy('SQSPollerPolicy', {'QueueName': 'my-first-queue'})
        #pprint(result)
        assert 'Statement' in result

    def test_policy_with_intrinsic_parameter(self):
        """Confirm that policy with an intrinsic gives the same output as SAM"""
        intrinsic_name = 'Fn::GetAtt'
        parameters = {
            'QueueName': {intrinsic_name: ['MyFirstQueue','QueueName']}
        }
        result = policy.get_policy('SQSPollerPolicy', parameters)
        pprint(result)
        #print(yaml.dump(result))
        assert 'Statement' in result
        assert 'Resource' in result['Statement'][0]
        # Determined by experimentation with yaml.dump and sam validate --debug
        # Resource:
        #     Fn::Sub:
        #     - arn:${AWS::Partition}:sqs:${AWS::Region}:${AWS::AccountId}:${queueName}
        #     - queueName:
        #         Fn::GetAtt:
        #         - MyFirstQueue
        #         - QueueName
        resource_entity = result['Statement'][0]['Resource']
        assert 'Fn::Sub' in resource_entity
        # Two items:  The !Sub template and then parameters for same
        # queueName is a hard-coded string that comes from SQSPollerPolicy
        assert '${queueName}' in resource_entity['Fn::Sub'][0]
        # This shows we're setting the non-pseudo parameter
        assert 'queueName' in resource_entity['Fn::Sub'][1]
        assert resource_entity['Fn::Sub'][1]['queueName'][intrinsic_name][0] == 'MyFirstQueue'
        assert resource_entity['Fn::Sub'][1]['queueName'][intrinsic_name][1] == 'QueueName'


    def test_invalid_policy_name(self):
        """Confirm that an invalid policy name doesn't generate a policy"""
        with pytest.raises(TemplateNotFoundException):
            policy.get_policy('NoSuchPolicyInSAM', {})
