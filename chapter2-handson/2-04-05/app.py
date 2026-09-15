#!/usr/bin/env python3
import aws_cdk as cdk
from visitor_counter_app.visitor_counter_app_stack import VisitorCounterAppStack
from visitor_counter_app.stacks.visitor_counter_stack import VisitorCounterStack

app = cdk.App()

# 移行が完了するまでは旧StackもAppへ残す
VisitorCounterAppStack(app, "VisitorCounterAppStack")
VisitorCounterStack(app, "VisitorCounterStack")

app.synth()
