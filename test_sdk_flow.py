import subprocess
import sys
import time


def run_command(command):
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    print(stdout.decode())
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(stderr.decode())
        sys.exit(1)
    return stdout.decode()


def main():
    print("Starting SDK install and test flow...")

    # Install the SDK
    print("Installing the SDK...")
    run_command("pip install .")

    # Create and run test script
    print("Creating test script...")
    test_script = """
import os
import time
from my_cache_sdk import Cache, UserContext

def test_cache(cache_type):
    print(f"Testing {cache_type} cache...")
    if cache_type == "dynamodb":
        cache = Cache(service="dynamodb", table_name="test_table", region_name="us-east-1")
    elif cache_type == "redis":
        cache = Cache(service="redis", host="localhost", port=6379)
    else:
        cache = Cache(service="memory")

    context = UserContext(customer_id="test_customer", tenant_id="test_tenant")
    
    # Test set and get
    print("Testing set and get operations...")
    cache.set("test_key", "test_value", context)
    value = cache.get("test_key", context)
    assert value == "test_value", f"Expected 'test_value', but got {value}"
    print(f"Retrieved value: {value}")
    
    # Test TTL
    print("Testing TTL...")
    cache.set("ttl_key", "ttl_value", context, ttl=2)
    value = cache.get("ttl_key", context)
    assert value == "ttl_value", f"Expected 'ttl_value', but got {value}"
    print("Waiting for TTL to expire...")
    time.sleep(3)
    value = cache.get("ttl_key", context)
    assert value is None, f"Expected None, but got {value}"
    print("TTL test passed")
    
    # Test delete
    print("Testing delete operation...")
    cache.set("delete_key", "delete_value", context)
    cache.delete("delete_key", context)
    value = cache.get("delete_key", context)
    assert value is None, f"Expected None, but got {value}"
    print("Delete test passed")
    
    print(f"{cache_type.capitalize()} cache test passed!")

if __name__ == "__main__":
    # Set up mock AWS credentials for DynamoDB testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    test_cache("memory")
    test_cache("redis")
    test_cache("dynamodb")
    """

    with open("temp_test_script.py", "w") as f:
        f.write(test_script)

    print("Running test script...")
    run_command("python temp_test_script.py")

    # Clean up
    print("Cleaning up...")
    run_command("rm temp_test_script.py")

    print("SDK install and test flow completed successfully!")


if __name__ == "__main__":
    main()
