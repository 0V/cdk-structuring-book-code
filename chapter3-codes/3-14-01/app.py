#!/usr/bin/env python3
import aws_cdk as cdk

from comparison_app.comparison_app_stack import ComparisonAppStack

app = cdk.App()
ComparisonAppStack(app, "ComparisonAppStack")
app.synth()
