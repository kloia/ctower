# https://docs.aws.amazon.com/controltower/latest/userguide/control-identifiers.html

guardrail_arn_fmt = "arn:aws:controltower:{region}::control/{control_identifier}"


def generate_guardrail_arn(control_identifier, region):
    return guardrail_arn_fmt.format(
        region=region, control_identifier=control_identifier
    )


ELECTIVE_GUARDRAILS = [
    {
        "id": "AWS-GR_AUDIT_BUCKET_ENCRYPTION_ENABLED",
        "text": "Disallow Changes to Encryption Configuration for Amazon S3 Buckets",
    },
    {
        "id": "AWS-GR_AUDIT_BUCKET_LOGGING_ENABLED",
        "text": "Disallow Changes to Logging Configuration for Amazon S3 Buckets",
    },
    {
        "id": "AWS-GR_AUDIT_BUCKET_POLICY_CHANGES_PROHIBITED",
        "text": "Disallow Changes to Bucket Policy for Amazon S3 Buckets",
    },
    {
        "id": "AWS-GR_AUDIT_BUCKET_RETENTION_POLICY",
        "text": "Disallow Changes to Lifecycle Configuration for Amazon S3 Buckets",
    },
    {
        "id": "AWS-GR_IAM_USER_MFA_ENABLED",
        "text": "Detect Whether MFA is Enabled for AWS IAM Users",
    },
    {
        "id": "AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS",
        "text": "Detect Whether MFA is Enabled for AWS IAM Users of the AWS Console",
    },
    {
        "id": "AWS-GR_RESTRICT_S3_CROSS_REGION_REPLICATION",
        "text": "Disallow Changes to Replication Configuration for Amazon S3 Buckets",
    },
    {
        "id": "AWS-GR_RESTRICT_S3_DELETE_WITHOUT_MFA",
        "text": "Disallow Delete Actions on Amazon S3 Buckets Without MFA",
    },
    {
        "id": "AWS-GR_S3_VERSIONING_ENABLED",
        "text": "Detect Whether Versioning for Amazon S3 Buckets is Enabled",
    },
]

DATA_RESIDENCY_GUARDRAILS = [
    {
        "id": "AWS-GR_SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED",
        "text": "Detect whether any Amazon VPC subnets are assigned a public IP address",
    },
    {
        "id": "AWS-GR_AUTOSCALING_LAUNCH_CONFIG_PUBLIC_IP_DISABLED",
        "text": "Detect whether public IP addresses for Amazon EC2 autoscaling are enabled through launch configurations",
    },
    {
        "id": "AWS-GR_DISALLOW_CROSS_REGION_NETWORKING",
        "text": "Disallow cross-region networking for Amazon EC2, Amazon CloudFront, and AWS Global Accelerator",
    },
    {
        "id": "AWS-GR_DISALLOW_VPC_INTERNET_ACCESS",
        "text": "Disallow internet access for an Amazon VPC instance managed by a customer",
    },
    {
        "id": "AWS-GR_DISALLOW_VPN_CONNECTIONS",
        "text": "Disallow Amazon Virtual Private Network (VPN) connections",
    },
    {
        "id": "AWS-GR_DMS_REPLICATION_NOT_PUBLIC",
        "text": "Detect whether replication instances for AWS Database Migration Service are public",
    },
    {
        "id": "AWS-GR_EBS_SNAPSHOT_PUBLIC_RESTORABLE_CHECK",
        "text": "Detect whether Amazon EBS snapshots are restorable by all AWS accounts",
    },
    {
        "id": "AWS-GR_EC2_INSTANCE_NO_PUBLIC_IP",
        "text": "Detect whether any Amazon EC2 instance has an associated public IPv4 address",
    },
    {
        "id": "AWS-GR_EKS_ENDPOINT_NO_PUBLIC_ACCESS",
        "text": "Detects whether an Amazon EKS endpoint is blocked from public access",
    },
    {
        "id": "AWS-GR_ELASTICSEARCH_IN_VPC_ONLY",
        "text": "Detect whether an Amazon OpenSearch Service domain is in Amazon VPC",
    },
    {
        "id": "AWS-GR_EMR_MASTER_NO_PUBLIC_IP",
        "text": "Detect whether any Amazon EMR cluster master nodes have public IP addresses",
    },
    {
        "id": "AWS-GR_LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED",
        "text": "Detect whether the AWS Lambda function policy attached to the Lambda resource blocks public access",
    },
    {
        "id": "AWS-GR_NO_UNRESTRICTED_ROUTE_TO_IGW",
        "text": "Detect whether public routes exist in the route table for an Internet Gateway (IGW)",
    },
    {
        "id": "AWS-GR_REDSHIFT_CLUSTER_PUBLIC_ACCESS_CHECK",
        "text": "Detect whether Amazon Redshift clusters are blocked from public access",
    },
    {
        "id": "AWS-GR_S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC",
        "text": "Detect whether Amazon S3 settings to block public access are set as true for the account",
    },
    {
        "id": "AWS-GR_SAGEMAKER_NOTEBOOK_NO_DIRECT_INTERNET_ACCESS",
        "text": "Detect whether an Amazon SageMaker notebook instance allows direct internet access",
    },
    {
        "id": "AWS-GR_SSM_DOCUMENT_NOT_PUBLIC",
        "text": "Detect whether AWS Systems Manager documents owned by the account are public",
    },
]

STRONGLY_RECOMMENDED_GUARDRAILS = [
    {
        "id": "AWS-GR_ENCRYPTED_VOLUMES",
        "text": "Detect Whether Encryption is Enabled for Amazon EBS Volumes Attached to Amazon EC2 Instances",
    },
    {
        "id": "AWS-GR_EBS_OPTIMIZED_INSTANCE",
        "text": "Detect Whether Amazon EBS Optimization is Enabled for Amazon EC2 Instances",
    },
    {
        "id": "AWS-GR_EC2_VOLUME_INUSE_CHECK",
        "text": "Detect Whether Amazon EBS Volumes are Attached to Amazon EC2 Instances",
    },
    {
        "id": "AWS-GR_RDS_INSTANCE_PUBLIC_ACCESS_CHECK",
        "text": "Detect Whether Public Access to Amazon RDS Database Instances is Enabled",
    },
    {
        "id": "AWS-GR_RDS_SNAPSHOTS_PUBLIC_PROHIBITED",
        "text": "Detect Whether Public Access to Amazon RDS Database Snapshots is Enabled",
    },
    {
        "id": "AWS-GR_RDS_STORAGE_ENCRYPTED",
        "text": "Detect Whether Storage Encryption is Enabled for Amazon RDS Database Instances",
    },
    {
        "id": "AWS-GR_RESTRICTED_COMMON_PORTS",
        "text": "Detect Whether Unrestricted Incoming TCP Traffic is Allowed",
    },
    {
        "id": "AWS-GR_RESTRICTED_SSH",
        "text": "Detect Whether Unrestricted Internet Connection Through SSH is Allowed",
    },
    {"id": "AWS-GR_RESTRICT_ROOT_USER", "text": "Disallow Actions as a Root User"},
    {
        "id": "AWS-GR_RESTRICT_ROOT_USER_ACCESS_KEYS",
        "text": "Disallow Creation of Access Keys for the Root User",
    },
    {
        "id": "AWS-GR_ROOT_ACCOUNT_MFA_ENABLED",
        "text": "Detect Whether MFA for the Root User is Enabled",
    },
    {
        "id": "AWS-GR_S3_BUCKET_PUBLIC_READ_PROHIBITED",
        "text": "Detect Whether Public Read Access to Amazon S3 Buckets is Allowed",
    },
    {
        "id": "AWS-GR_S3_BUCKET_PUBLIC_WRITE_PROHIBITED",
        "text": "Detect Whether Public Write Access to Amazon S3 Buckets is Allowed",
    },
    {
        "id": "AWS-GR_ENSURE_CLOUDTRAIL_ENABLED_ON_MEMBER_ACCOUNTS",
        "text": "Detect whether an account has AWS CloudTrail or CloudTrail Lake enabled",
    },
]

ALL_GUARDRAILS = (
    ELECTIVE_GUARDRAILS + DATA_RESIDENCY_GUARDRAILS + STRONGLY_RECOMMENDED_GUARDRAILS
)

MANDATORY_CONTROL_TOWER_GUARDRAILS = [
    {"id": "AWS-GR_CLOUDTRAIL_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CLOUDTRAIL_CLOUDWATCH_LOGS_ENABLED", "text": ""},
    {"id": "AWS-GR_CLOUDTRAIL_ENABLED", "text": ""},
    {"id": "AWS-GR_CLOUDTRAIL_VALIDATION_ENABLED", "text": ""},
    {"id": "AWS-GR_CLOUDWATCH_EVENTS_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CONFIG_AGGREGATION_AUTHORIZATION_POLICY", "text": ""},
    {"id": "AWS-GR_CONFIG_AGGREGATION_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CONFIG_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CONFIG_ENABLED", "text": ""},
    {"id": "AWS-GR_CONFIG_RULE_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_IAM_ROLE_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_LAMBDA_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_LOG_GROUP_POLICY", "text": ""},
    {"id": "AWS-GR_SNS_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_SNS_SUBSCRIPTION_CHANGE_PROHIBITED", "text": ""},
]


NON_CONTROL_TOWER_GUARDRAILS = [
    {"id": "AWS-GR_REGION_DENY", "text": ""},
    {"id": "AWS-GR_AUDIT_BUCKET_DELETION_PROHIBITED", "text": ""},
    {"id": "AWS-GR_AUDIT_BUCKET_PUBLIC_READ_PROHIBITED", "text": ""},
    {"id": "AWS-GR_AUDIT_BUCKET_PUBLIC_WRITE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CLOUDTRAIL_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CLOUDTRAIL_CLOUDWATCH_LOGS_ENABLED", "text": ""},
    {"id": "AWS-GR_CLOUDTRAIL_ENABLED", "text": ""},
    {"id": "AWS-GR_CLOUDTRAIL_VALIDATION_ENABLED", "text": ""},
    {"id": "AWS-GR_CLOUDWATCH_EVENTS_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CONFIG_AGGREGATION_AUTHORIZATION_POLICY", "text": ""},
    {"id": "AWS-GR_CONFIG_AGGREGATION_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CONFIG_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CONFIG_ENABLED", "text": ""},
    {"id": "AWS-GR_CONFIG_RULE_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_CT_AUDIT_BUCKET_ENCRYPTION_CHANGES_PROHIBITED", "text": ""},
    {
        "id": "AWS-GR_CT_AUDIT_BUCKET_LIFECYCLE_CONFIGURATION_CHANGES_PROHIBITED",
        "text": "",
    },
    {
        "id": "AWS-GR_CT_AUDIT_BUCKET_LOGGING_CONFIGURATION_CHANGES_PROHIBITED",
        "text": "",
    },
    {"id": "AWS-GR_CT_AUDIT_BUCKET_POLICY_CHANGES_PROHIBITED", "text": ""},
    {"id": "AWS-GR_IAM_ROLE_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_LAMBDA_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_LOG_GROUP_POLICY", "text": ""},
    {"id": "AWS-GR_SNS_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_SNS_SUBSCRIPTION_CHANGE_PROHIBITED", "text": ""},
    {"id": "AWS-GR_ENSURE_CLOUDTRAIL_ENABLED_ON_SHARED_ACCOUNTS", "text": ""},
]
