import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3LifecycleManager:
    def __init__(self, bucket_names):
        self.bucket_names = bucket_names
        self.s3_client = boto3.client('s3')

    def put_lifecycle_policy(self, lifecycle_policy):
        for bucket_name in self.bucket_names:
            try:
                self.s3_client.put_bucket_lifecycle_configuration(
                    Bucket=bucket_name,
                    LifecycleConfiguration=lifecycle_policy
                )
                print(f"Lifecycle policy applied to bucket {bucket_name}.")
            except (NoCredentialsError, PartialCredentialsError):
                print("Error: AWS credentials not found.")
            except Exception as e:
                print(f"An error occurred for bucket {bucket_name}: {e}")

    def get_lifecycle_policy(self):
        for bucket_name in self.bucket_names:
            try:
                response = self.s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                print(f"Current lifecycle policy for bucket {bucket_name}: {response['Rules']}")
            except self.s3_client.exceptions.NoSuchLifecycleConfiguration:
                print(f"No lifecycle policy found for bucket {bucket_name}.")
            except (NoCredentialsError, PartialCredentialsError):
                print("Error: AWS credentials not found.")
            except Exception as e:
                print(f"An error occurred for bucket {bucket_name}: {e}")

    def delete_lifecycle_policy(self):
        for bucket_name in self.bucket_names:
            try:
                self.s3_client.delete_bucket_lifecycle(Bucket=bucket_name)
                print(f"Lifecycle policy deleted from bucket {bucket_name}.")
            except (NoCredentialsError, PartialCredentialsError):
                print("Error: AWS credentials not found.")
            except Exception as e:
                print(f"An error occurred for bucket {bucket_name}: {e}")

# Function to load lifecycle policy from a JSON file
def load_lifecycle_policy(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

# Example usage:
if __name__ == "__main__":
    bucket_names = [
        "s3-lifecycle-sleeping-knight-1",
        "s3-lifecycle-sleeping-knight-2"
    ]
    json_file_path = 'policy/lifecycle-policy.json'
    lifecycle_policy = load_lifecycle_policy(json_file_path)

    s3_lifecycle_manager = S3LifecycleManager(bucket_names)

    # Put lifecycle policy
    s3_lifecycle_manager.put_lifecycle_policy(lifecycle_policy)

    # # Get lifecycle policy
    # policy = s3_lifecycle_manager.get_lifecycle_policy()
    # if policy:
    #     print("Current lifecycle policy:", policy)

    # # Delete lifecycle policy
    # s3_lifecycle_manager.delete_lifecycle_policy()

