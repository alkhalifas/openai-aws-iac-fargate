from aws_cdk import (
    Stack,
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

        # Use ALB + Fargate from ECS patterns
        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'MyFlaskApiWithFargate',
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            assign_public_ip=True,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset('./server'),
                container_port=8000),
            public_load_balancer=True,
            # Since no specific domain is used, HTTPS configuration is removed
            protocol=elb_v2.ApplicationProtocol.HTTP
        )

        # Default target group healthcheck path is '/'
        service.target_group.configure_health_check(path='/health')
