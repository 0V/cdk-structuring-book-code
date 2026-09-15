#!/usr/bin/env python3
import aws_cdk as cdk
from visitor_counter_app.stacks.visitor_counter_stack import VisitorCounterStack
from visitor_counter_app.stacks.report_stack import ReportStack

app = cdk.App()

visitor_counter_stack = VisitorCounterStack(app, "VisitorCounterStack")

# テーブルのオブジェクトを直接渡す
report_stack = ReportStack(app, "ReportStack",
    visits_table=visitor_counter_stack.table,
)

# 依存関係はオブジェクト参照から自動導出されるが、意図を明示するために記述する
report_stack.add_dependency(visitor_counter_stack)

app.synth()
