#!/usr/bin/env python3
import aws_cdk as cdk
from visitor_counter_app.stacks.visitor_counter_stack import VisitorCounterStack
from visitor_counter_app.stacks.report_stack import ReportStack

app = cdk.App()
visitor_counter_stack = VisitorCounterStack(app, "VisitorCounterStack")
report_stack = ReportStack(app, "ReportStack")

# SSMパラメータ名を文字列で参照しているため、CDKはStack間の依存関係を推論できない。
# ReportStackが先にデプロイされるとパラメータが存在せず失敗するため、明示的に指定する
report_stack.add_dependency(visitor_counter_stack)

app.synth()
