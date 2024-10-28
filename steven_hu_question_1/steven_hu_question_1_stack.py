from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_sqs as sqs,
)
from constructs import Construct


class StevenHuQuestion1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 建立 SQS 佇列
        queue = sqs.Queue(self, "StevenHuQuestion1Queue")

        # 建立 Lambda 函數處理 POST 請求
        post_function = lambda_.Function(
            self,
            "PostFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="lambda_functions.post_handler",
            code=lambda_.Code.from_asset("lambda"),
        )

        # 建立 Lambda 函數處理 GET 請求
        get_function = lambda_.Function(
            self,
            "GetFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="lambda_functions.get_handler",
            code=lambda_.Code.from_asset("lambda"),
        )

        # 授權 POST, GET 函數發送、接收消息至 SQS 佇列
        queue.grant_send_messages(post_function)
        queue.grant_consume_messages(get_function)

        # 建立 API Gateway
        api = apigateway.RestApi(self, "StevenHuQuestion1Api")

        # 將 POST, GET 函數與 API Gateway 整合
        post_integration = apigateway.LambdaIntegration(post_function)
        get_integration = apigateway.LambdaIntegration(get_function)

        # 在 API Gateway 添加 POST, GET 方法
        api.root.add_method("POST", post_integration)
        api.root.add_method("GET", get_integration)

        # 將 SQS 佇列的 URL 傳遞給 POST, GET 函數
        post_function.add_environment("QUEUE_URL", queue.queue_url)
        get_function.add_environment("QUEUE_URL", queue.queue_url)
