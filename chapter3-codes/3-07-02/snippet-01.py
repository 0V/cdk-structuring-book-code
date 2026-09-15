# Blackによるフォーマット後
import os
import aws_cdk as cdk
from constructs import Construct
import json


def create_bucket(name: str, region: str) -> None:
    unused_variable = "この変数は使われていない"
    print("Creating bucket: " + name)
