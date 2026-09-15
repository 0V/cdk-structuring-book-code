#!/usr/bin/env python3
import aws_cdk as cdk

from visitor_counter_app.visitor_counter_app_stack import VisitorCounterAppStack

app = cdk.App()
VisitorCounterAppStack(app, "VisitorCounterAppStack")

app.synth()
