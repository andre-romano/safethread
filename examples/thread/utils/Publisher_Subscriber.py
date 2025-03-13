
from safethread.thread.utils import Publisher, Subscriber

result = "Hello from "


def replace_result_with(data):
    global result
    result = data


def append_to_result(data):
    global result
    result = result + data


subscriber1 = Subscriber(replace_result_with)
subscriber2 = Subscriber(append_to_result)

publisher = Publisher()
publisher.subscribe(subscriber1)
publisher.subscribe(subscriber2)

test_data = "New Data "
publisher.publish(test_data)
print(f"Result: {result} - Expected output: New Data New Data")

# reset result variable
result = "Hello from "

publisher.unsubscribe(subscriber1)

test_data = "TestUnit"
publisher.publish(test_data)
print(f"Result: {result} - Expected output: Hello from TestUnit")
