import aws_cdk as core
import aws_cdk.assertions as assertions

from visitor_counter_app.stacks.visitor_counter_stack import VisitorCounterStack

# example tests. To run these tests, uncomment this file along with the example
# resource in visitor_counter_app/visitor_counter_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = VisitorCounterStack(app, "visitor-counter-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
