import faker
import grpc
import location_pb2
import location_pb2_grpc

"""
Sample gRPC client implementation that demonstrates how a
mobile device can communicate with gRPC
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("127.0.0.1:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

preloaded_person_ids = [1, 5, 6, 8, 9]
non_existing_person_ids = [987, 56]

fake = faker.Faker()

def random_float_str():
    return str(fake.pyfloat(1))

# Send the desired payload to existing and non-existing people
payloads = [location_pb2.LocationMessage(person_id=y, latitude=random_float_str(), longitude=random_float_str()) for x in [preloaded_person_ids, non_existing_person_ids] for y in x]

for location in payloads:
    response = stub.Create(location)
    print(f"Response from gRPC server: {response}")