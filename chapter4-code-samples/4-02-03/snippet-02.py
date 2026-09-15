class AuthenticationConstruct(Construct):
    """認証機能のConstruct"""
    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)

        # 認証に必要なリソースのみを定義
        self.user_pool = cognito.UserPool(self, "UserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True))
        self.user_pool_client = self.user_pool.add_client("AppClient")

class NotificationConstruct(Construct):
    """通知機能のConstruct"""
    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)

        # 通知に必要なリソースのみを定義
        self.topic = sns.Topic(self, "NotificationTopic")
        self.queue = sqs.Queue(self, "NotificationQueue")
        self.topic.add_subscription(subscriptions.SqsSubscription(self.queue))
