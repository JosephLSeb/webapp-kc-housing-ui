import json
from loadimpact import (
    HttpTest,
    UserScenario,
    ParallelTask,
    SequentialTask,
    ApiTokenCredential,
    DataParameter,
    ResponseTimeMetric,
    ResponseCodeMetric,
    CustomMetric,
)


# Define the API endpoint URL
endpoint_url = "http://127.0.0.1:5000/analysis"

# Define the sample input array
input_array = {"bedrooms": 3, "price_range": 1}

# Define the user scenario for the load test
scenario = UserScenario(name="Flask web app load test")

# Define the HTTP test step
http_test = HttpTest(name="Flask web app test", endpoint=endpoint_url, method="POST")
http_test.set_request_body(json.dumps(input_array))
http_test.add_request_header("Content-Type", "application/json")
http_test.add_response_metric(ResponseTimeMetric())
http_test.add_response_metric(ResponseCodeMetric())
http_test.add_custom_metric(
    CustomMetric(
        name="Custom metric",
        unit="requests/sec",
        type="rate",
        provider="http",
        query="rpm",
        aggregation="sum",
    )
)

# Define the user scenario tasks
scenario.tasks = [
    ParallelTask(
        name="API requests",
        tasks=[
            SequentialTask(
                name="API request",
                requests=[http_test],
                weight=100,
            )
        ],
    )
]

# Define the test configuration
test_config = {
    "name": "Flask web app load test",
    "type": "simple",
    "user_type": "basic",
    "credential": ApiTokenCredential("40360755c403612e2e2548f44fa0318fcf60f97c2718bf7f0b2eff9f4a9ba0ed"),
    "server_id": "3e60bfe3f00cadd63c4203e5125f76b930daed7a5737ad9e1da18df519bba358",
    "test_id": "40360755c403612e2e2548f44fa0318fcf60f97c2718bf7f0b2eff9f4a9ba0ed",
    "user_scenario": scenario,
    "data": [DataParameter(name="input_array", values=[json.dumps(input_array)])],
}

# Start the load test
test_result = HttpTest.start_test(test_config)

# Print the test results
print("Test result: ", test_result)
print("Metrics: ", test_result.metrics)

