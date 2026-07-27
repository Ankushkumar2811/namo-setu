data "aws_availability_zones" "available" {state = "available"}
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
  tags = {Name = local.name}
}
resource "aws_subnet" "private" {
  count = 3
  vpc_id = aws_vpc.main.id
  cidr_block = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags = {Name = "${local.name}-private-${count.index + 1}"}
}
resource "aws_db_subnet_group" "main" {
  name = local.name
  subnet_ids = aws_subnet.private[*].id
}
resource "aws_security_group" "data" {
  name = "${local.name}-data"
  vpc_id = aws_vpc.main.id
}
resource "aws_rds_cluster" "postgres" {
  cluster_identifier = "${local.name}-postgres"
  engine = "aurora-postgresql"
  engine_mode = "provisioned"
  database_name = "namo_setu"
  master_username = "namo_admin"
  manage_master_user_password = true
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.data.id]
  storage_encrypted = true
  backup_retention_period = 35
  preferred_backup_window = "18:00-19:00"
  deletion_protection = true
  enabled_cloudwatch_logs_exports = ["postgresql"]
  skip_final_snapshot = false
}
resource "aws_rds_cluster_instance" "postgres" {
  count = 2
  identifier = "${local.name}-postgres-${count.index + 1}"
  cluster_identifier = aws_rds_cluster.postgres.id
  instance_class = var.db_instance_class
  engine = aws_rds_cluster.postgres.engine
}
resource "aws_elasticache_subnet_group" "main" {
  name = local.name
  subnet_ids = aws_subnet.private[*].id
}
resource "aws_elasticache_replication_group" "redis" {
  replication_group_id = "${local.name}-redis"
  description = "NAMO SETU cache and realtime fan-out"
  node_type = var.redis_node_type
  port = 6379
  subnet_group_name = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.data.id]
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  automatic_failover_enabled = true
  multi_az_enabled = true
  num_cache_clusters = 2
  snapshot_retention_limit = 7
}
resource "aws_s3_bucket" "media" {
  bucket_prefix = "${local.name}-media-"
}
resource "aws_s3_bucket_versioning" "media" {
  bucket = aws_s3_bucket.media.id
  versioning_configuration {status = "Enabled"}
}
resource "aws_s3_bucket_server_side_encryption_configuration" "media" {
  bucket = aws_s3_bucket.media.id
  rule {apply_server_side_encryption_by_default {sse_algorithm = "aws:kms"}}
}
resource "aws_s3_bucket_public_access_block" "media" {
  bucket = aws_s3_bucket.media.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
