from aws_cdk import (
    Stack, Tags,
    aws_ssm as ssm,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elb_v2,
)
from constructs import Construct


class OpenaiAwsIacFargateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve VPC information
        vpc = ec2.Vpc.from_lookup(
            self, 'VPC',
            is_default=True)

        # ECS cluster
        cluster = ecs.Cluster(self, 'MyCluster', vpc=vpc)

        # ECS task with the OpenAI API key as a secret
        task_image_options = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_asset('./server'),
            container_port=8000,
            secrets={
                'OPENAI_API_KEY': ecs.Secret.from_ssm_parameter(
                    ssm.StringParameter.from_secure_string_parameter_attributes(
                        self, "OpenAIParam",
                        parameter_name="OPENAI_API_KEY",
                        # version is optional, remove if you always want the latest version
                        version=1
                    )
                )
            }
        )

        # Use ALB + Fargate from ECS patterns
        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'FastApiWithFargate',
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            assign_public_ip=True,
            task_image_options=task_image_options,
            public_load_balancer=True,
            # Since no specific domain is used, HTTPS configuration is removed
            protocol=elb_v2.ApplicationProtocol.HTTP
        )

        # Default target group healthcheck path is '/'
        service.target_group.configure_health_check(path='/health')

        # Add tags to all resources in this stack
        Tags.of(self).add("Project", "Medium")
        Tags.of(self).add("Environment", "Development")
