import argparse
import json
import os
import subprocess
import sys


def assume_role(role_arn: str, profile: str, session_name: str) -> None:
    assume_role_response = subprocess.check_output([
        "aws", "sts", "assume-role",
        "--profile", profile,
        "--role-arn", role_arn,
        "--role-session-name", session_name
    ])

    result = json.loads(assume_role_response)
    print(f'export AWS_ACCESS_KEY_ID={result["Credentials"]["AccessKeyId"]}')
    print(f'export AWS_SECRET_ACCESS_KEY={result["Credentials"]["SecretAccessKey"]}')
    print(f'export AWS_SESSION_TOKEN={result["Credentials"]["SessionToken"]}')


if __name__ == "__main__":
    """
    This script assists in setting up AWS credentials for an assumed role in your environment. Since Python scripts 
    cannot alter the parent shell environment, the script generates output that should be evaluated to load the 
    credentials into your environment.

    This script utilizes built-in packages, and thus eliminates the need for third-party dependencies. The script 
    assumes that the AWS Command Line Interface (AWS CLI) is already installed in the environment.
    
    Usage
        export AWS_ROLE_TO_ASSUME=arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME
        $(python3 set_aws_creds.py):
    Or
        $(python3 set_aws_creds.py --role arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=False, default=os.environ.get('AWS_ROLE_TO_ASSUME'), help="Role ARN to assume. Can be passed as command argument or set as env variable 'AWS_ROLE_TO_ASSUME'")
    parser.add_argument("--session", default="scripted_session", help="Session name. Optional, defaults to 'scripted_session'")
    parser.add_argument("--profile", default='default', help="AWS Profile to use. Optional, defaults to 'default'")
    args = parser.parse_args()

    if args.role:
        assume_role(args.role, args.profile, args.session)
    else:
        print("Error: Please provide a Role ARN as argument (--role) or set AWS_ROLE_TO_ASSUME environment variable.")
        sys.exit(1)
