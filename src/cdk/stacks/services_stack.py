from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct
import os

class ServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        secret = secretsmanager.Secret.from_secret_name_v2(
            self, "SeekTodoListSecret", secret_name="seek/todo-list"
        )

        lambda_code = lambda_.Code.from_asset(os.path.join(os.getcwd(), ".."))

        lambda_function = lambda_.Function(
            self, "SeekTodoList",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="main.lambda_handler",
            code=lambda_code,
            environment={
                "MONGODB_URI": secret.secret_value_from_json("MONGODB_URI").to_string(),
                "JWT_SECRET_KEY": secret.secret_value_from_json("JWT_SECRET_KEY").to_string(),
            }
        )

        api = apigateway.LambdaRestApi(
            self, "SeekTodoListApiGw",
            handler=lambda_function,
            proxy=False
        )

        v1_resource = api.root.add_resource("v1")

        # tasks
        tasks_resource = v1_resource.add_resource("tasks")
        tasks_resource.add_method("GET")  # GET /v1/tasks
        task_resource = tasks_resource.add_resource("{task_id}")
        task_resource.add_method("GET")  # GET /v1/tasks/:task_id
        task_resource.add_method("PUT")  # PUT /v1/tasks/:task_id
        tasks_resource.add_method("POST")  # POST /v1/tasks

        # auth
        auth_resource = v1_resource.add_resource("auth")
        auth_register = auth_resource.add_resource("register")
        auth_register.add_method("POST")  # POST /v1/auth/register
        auth_login = auth_resource.add_resource("login")
        auth_login.add_method("POST")  # POST /v1/auth/login

        lambda_function.grant_invoke(iam.ServicePrincipal("apigateway.amazonaws.com"))
