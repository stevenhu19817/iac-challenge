import aws_cdk as core
import aws_cdk.assertions as assertions

from steven_hu_question_1.steven_hu_question_1_stack import StevenHuQuestion1Stack


# example tests. To run these tests, uncomment this file along with the example
# resource in steven_hu_question_1/steven_hu_question_1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = StevenHuQuestion1Stack(app, "steven-hu-question-1")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
