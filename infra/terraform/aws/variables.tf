variable "aws_region" {type = string; default = "ap-south-1"}
variable "environment" {type = string; default = "production"}
variable "vpc_cidr" {type = string; default = "10.40.0.0/16"}
variable "db_instance_class" {type = string; default = "db.r7g.large"}
variable "redis_node_type" {type = string; default = "cache.r7g.large"}
variable "allowed_frontend_origin" {type = string; default = "https://namo-setu.vercel.app"}
locals {
  name = "namo-setu-${var.environment}"
  tags = {Project = "namo-setu", Environment = var.environment, ManagedBy = "terraform"}
}
