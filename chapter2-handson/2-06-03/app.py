#!/usr/bin/env python3
import aws_cdk as cdk
from visitor_counter_app.stacks.visitor_counter_stack import VisitorCounterStack
from visitor_counter_app.stacks.report_stack import ReportStack

app = cdk.App()
visitor_counter_stack = VisitorCounterStack(app, "VisitorCounterStack")
report_stack = ReportStack(app, "ReportStack")
app.synth()
