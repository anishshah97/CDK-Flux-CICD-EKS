#!/usr/bin/env python3

from aws_cdk import core
from dockerpipeline.docker_pipeline import DockerPipelineConstruct
from fluxcd.fluxcd_construct import FluxcdConstruct
from cluster.cluster_construct import ClusterConstruct
import os

# codecommit credentials
codecommit_git_auth_user = os.environ["CODECOMMIT_GIT_AUTH_USER"]
codecommit_git_auth_key = os.environ["CODECOMMIT_GIT_AUTH_KEY"]

# github credentials
github_oauth_token = os.environ["GITHUB_OAUTH_TOKEN"]

app = core.App()

name = app.node.try_get_context("name")
region = app.node.try_get_context("region")

aws_env = core.Environment(region=region)
stack = core.Stack(scope=app, id=f"{name}-stack", env=aws_env)

cluster_construct = ClusterConstruct(
    scope=stack,
    id=f"{name}-cluster",
    cluster_name=f"{name}-cluster"
)
fluxcd_docker_pipeline = DockerPipelineConstruct(
    scope=stack,
    id=f"{name}-docker-pipeline"
)
fluxcd_construct = FluxcdConstruct(
    scope=stack,
    id=f"{name}-fluxcd",
    git_user=codecommit_git_auth_user,
    git_password=codecommit_git_auth_key,
    eks_base_cluster=cluster_construct.cluster
)

app.synth()
