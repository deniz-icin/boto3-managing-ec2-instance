import boto3
import sys

EC2_RESOURCE = boto3.resource('ec2')
EC2_CLIENT = boto3.client("ec2")

def is_response_successful(response):
    status_code = response.get('ResponseMetadata').get('HTTPStatusCode')
    if 200 <= status_code < 300 :
        return True
    return False

def list_all_instances():
    response = EC2_CLIENT.describe_instances()
    success = is_response_successful(response)
    if success is False: print("Connection failed.")
    instances = EC2_RESOURCE.instances.all()
    instance_string = [
        "Instance ID = {:^30s} |   Public IPv4 address: {:^15s} |   Instance State : {:>10s}".format(instance.id,str(instance.public_ip_address),instance.state['Name'])
        for instance in instances
    ]
    if len(instance_string) == 0 :
        print("There is no instance running or stopped. \n")
        sys.exit()
    print("\n".join(instance_string))

def stop_instance(instance_id):
    instance = EC2_RESOURCE.Instance(instance_id)
    try:
        instance.stop()
        print(f"Stopping EC2 instance: {instance_id}")
        instance.wait_until_stopped()
        print(f'EC2 instance "{instance_id}" has been stopped')
    except:
        print("\n ID wrong! Please type valid instance ID. \n")
        return get_input()

def terminate_instance(instance_id):
    instance = EC2_RESOURCE.Instance(instance_id)
    try:
        instance.terminate()
        print(f"Terminating EC2 instance: {instance_id}")
        instance.wait_until_terminated()
        print(f'EC2 instance "{instance_id}" has been terminated')
    except:
        print("\n ID wrong! Please type valid instance ID. \n")
        return get_input()

def start_instance(instance_id):
    instance = EC2_RESOURCE.Instance(instance_id)
    try:
        instance.start()
        print(f"Starting EC2 instance: {instance_id}")
        instance.wait_until_running()
        print(f'EC2 instance "{instance_id}" has been started')
    except:
        print("\n ID wrong! Please type valid instance ID. \n")
        return get_input()

def get_input():
    instance_id = input("You can start, stop or terminate your instances.\nFirst, which instance do you want to process?\nPlease enter instance id : ")
    operation = input("Please select the operation (start,stop,terminate): ")
    if operation == "start":
        start_instance(instance_id)
    elif operation == "stop":
        stop_instance(instance_id)
    elif operation == "terminate":
        terminate_instance(instance_id)
    else:
        print("\n Please enter a valid operation. \n")
        return get_input()
        
def main():
    print('\n')
    list_all_instances()
    print('\n')
    get_input()
    do_again()

def do_again():
    again = input("Do you want to do anything else? (y/n):")
    if again == "n":
        sys.exit()
    elif again =="y":
        return main()
    print("\n You can only type (y) or (n).")
    return do_again()

if __name__ == "__main__":
    main()