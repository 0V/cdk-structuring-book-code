#!/usr/bin/env python3
import aws_cdk as cdk
from visitor_counter_app.stacks.visitor_counter_stack import VisitorCounterStack

app = cdk.App()
VisitorCounterStack(app, "VisitorCounterStack")
app.synth()
