#!/usr/bin/env python3
from aws_cdk import App
from stacks.services_stack import ServiceStack

app = App()
ServiceStack(app, "ServiceStack")

app.synth()
