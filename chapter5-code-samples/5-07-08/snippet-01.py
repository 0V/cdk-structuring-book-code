# ユニットテストの例
from aws_cdk import App
from aws_cdk.assertions import Template

from my_app.my_stack import MyStack


def test_lambda_function_has_correct_environment_variables():
    app = App()
    stack = MyStack(app, "TestStack", env_name="test")
    template = Template.from_stack(stack)

    # Lambda関数が正しい環境変数を持っているか確認
    template.has_resource_properties("AWS::Lambda::Function", {
        "Environment": {
            "Variables": {
                "TABLE_NAME": {"Ref": "MyTableCD117FA1"}
            }
        }
    })
