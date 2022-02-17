import datetime
from sqlite3 import Timestamp
from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import ClientSecretCredential

subscription_id = ""
resource_group_name = "traffic_manager_poc"
tm_name = "saroekTM"

# Get the ARM id of your resource. You might chose to do a "get"
# using the according management or to build the URL directly

resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Network/trafficManagerProfiles/{}"
).format(subscription_id, resource_group_name, tm_name)


def get_credentials():
    # with env_vars(https_proxy='http://%s' % self.csg_proxy,
    #                 REQUESTS_CA_BUNDLE=str(self.cacert_path)):
    creds = ClientSecretCredential(
        client_id="",
        client_secret="",
        tenant_id=""
    )
    return creds

# create client
client = MonitorManagementClient(
    get_credentials(),
    subscription_id
)

# You can get the available metrics of this specific resource
for metric in client.metric_definitions.list(resource_id):
    # azure.monitor.models.MetricDefinition
    print("{}: id={}, unit={}".format(
        metric.name.localized_value,
        metric.name.value,
        metric.unit
    ))

# Get Queries by Endpoint Returned (Count) of "2022-02-14" to "2022-02-17" for this TM, by hour

start = "2022-02-14"
end = "2022-02-18"

metrics_data = client.metrics.list(
    resource_id,
    timespan = "{}/{}".format(start, end),
    interval='PT1H',
    metricnames='QpsByEndpoint',
    aggregation='Total'
)

for item in metrics_data.value:
    # azure.mgmt.monitor.models.Metric
    print("{} ({})".format(item.name.localized_value, item.unit))
    # print(item)
    for timeserie in item.timeseries:
        # print(timeserie)
        for data in timeserie.data:
            # azure.mgmt.monitor.models.MetricData
            # print(data)
            print("{}: {}".format(data.time_stamp, data.total))

# Example of result:
# Queries by Endpoint Returned (Count) : number of queries that a Traffic Manager profile processes over a specified period

# 2022-02-14 00:00:00+00:00: 0.0
# 2022-02-14 01:00:00+00:00: 0.0
# 2022-02-14 02:00:00+00:00: 0.0
# 2022-02-14 03:00:00+00:00: 0.0
# 2022-02-14 04:00:00+00:00: 0.0
# 2022-02-14 05:00:00+00:00: 0.0
# 2022-02-14 06:00:00+00:00: 0.0
# 2022-02-14 07:00:00+00:00: 0.0
# 2022-02-14 08:00:00+00:00: 0.0
# 2022-02-14 09:00:00+00:00: 0.0
# 2022-02-14 10:00:00+00:00: 0.0
# 2022-02-14 11:00:00+00:00: 0.0
# 2022-02-14 12:00:00+00:00: 0.0
# 2022-02-14 13:00:00+00:00: 0.0
# 2022-02-14 14:00:00+00:00: 0.0
# 2022-02-14 15:00:00+00:00: 0.0
# 2022-02-14 16:00:00+00:00: 0.0
# 2022-02-14 17:00:00+00:00: 0.0
# 2022-02-14 18:00:00+00:00: 0.0
# 2022-02-14 19:00:00+00:00: 0.0
# 2022-02-14 20:00:00+00:00: 0.0
# 2022-02-14 21:00:00+00:00: 0.0
# 2022-02-14 22:00:00+00:00: 0.0
# 2022-02-14 23:00:00+00:00: 0.0
# 2022-02-15 00:00:00+00:00: 0.0
# 2022-02-15 01:00:00+00:00: 0.0
# 2022-02-15 02:00:00+00:00: 0.0
# 2022-02-15 03:00:00+00:00: 0.0
# 2022-02-15 04:00:00+00:00: 0.0
# 2022-02-15 05:00:00+00:00: 0.0
# 2022-02-15 06:00:00+00:00: 0.0
# 2022-02-15 07:00:00+00:00: 0.0
# 2022-02-15 08:00:00+00:00: 0.0
# 2022-02-15 09:00:00+00:00: 0.0
# 2022-02-15 10:00:00+00:00: 0.0
# 2022-02-15 11:00:00+00:00: 0.0
# 2022-02-15 12:00:00+00:00: 0.0
# 2022-02-15 13:00:00+00:00: 0.0
# 2022-02-15 14:00:00+00:00: 0.0
# 2022-02-15 15:00:00+00:00: 0.0
# 2022-02-15 16:00:00+00:00: 0.0
# 2022-02-15 17:00:00+00:00: 0.0
# 2022-02-15 18:00:00+00:00: 0.0
# 2022-02-15 19:00:00+00:00: 0.0
# 2022-02-15 20:00:00+00:00: 0.0
# 2022-02-15 21:00:00+00:00: 0.0
# 2022-02-15 22:00:00+00:00: 2.0
# 2022-02-15 23:00:00+00:00: 0.0

metrics_data = client.metrics.list(
    resource_id,
    timespan = "{}/{}".format(start, end),
    interval='PT1H',
    metricnames='ProbeAgentCurrentEndpointStateByProfileResourceId',
    aggregation='Maximum'
)

for item in metrics_data.value:
    # azure.mgmt.monitor.models.Metric
    print("{} ({})".format(item.name.localized_value, item.unit))
    # print(item)
    for timeserie in item.timeseries:
        # print(timeserie)
        for data in timeserie.data:
            # azure.mgmt.monitor.models.MetricData
            # print(data)
            print("{}: {}".format(data.time_stamp, data.maximum))

# Example of result: health status of the endpoints in the profile
# use 1 if the endpoint is up.
# use 0 if the endpoint is down.

# Endpoint Status by Endpoint (Count)
# 2022-02-14 00:00:00+00:00: None
# 2022-02-14 01:00:00+00:00: None
# 2022-02-14 02:00:00+00:00: None
# 2022-02-14 03:00:00+00:00: None
# 2022-02-14 04:00:00+00:00: None
# 2022-02-14 05:00:00+00:00: None
# 2022-02-14 06:00:00+00:00: None
# 2022-02-14 07:00:00+00:00: None
# 2022-02-14 08:00:00+00:00: None
# 2022-02-14 09:00:00+00:00: None
# 2022-02-14 10:00:00+00:00: None
# 2022-02-14 11:00:00+00:00: None
# 2022-02-14 12:00:00+00:00: None
# 2022-02-14 13:00:00+00:00: None
# 2022-02-14 14:00:00+00:00: None
# 2022-02-14 15:00:00+00:00: None
# 2022-02-14 16:00:00+00:00: None
# 2022-02-14 17:00:00+00:00: None
# 2022-02-14 18:00:00+00:00: None
# 2022-02-14 19:00:00+00:00: None
# 2022-02-14 20:00:00+00:00: None
# 2022-02-14 21:00:00+00:00: None
# 2022-02-14 22:00:00+00:00: None
# 2022-02-14 23:00:00+00:00: None
# 2022-02-15 00:00:00+00:00: None
# 2022-02-15 01:00:00+00:00: None
# 2022-02-15 02:00:00+00:00: None
# 2022-02-15 03:00:00+00:00: None
# 2022-02-15 04:00:00+00:00: None
# 2022-02-15 05:00:00+00:00: None
# 2022-02-15 06:00:00+00:00: None
# 2022-02-15 07:00:00+00:00: None
# 2022-02-15 08:00:00+00:00: None
# 2022-02-15 09:00:00+00:00: None
# 2022-02-15 10:00:00+00:00: None
# 2022-02-15 11:00:00+00:00: None
# 2022-02-15 12:00:00+00:00: None
# 2022-02-15 13:00:00+00:00: None
# 2022-02-15 14:00:00+00:00: None
# 2022-02-15 15:00:00+00:00: None
# 2022-02-15 16:00:00+00:00: None
# 2022-02-15 17:00:00+00:00: None
# 2022-02-15 18:00:00+00:00: None
# 2022-02-15 19:00:00+00:00: None
# 2022-02-15 20:00:00+00:00: None
# 2022-02-15 21:00:00+00:00: None
# 2022-02-15 22:00:00+00:00: 1.0
# 2022-02-15 23:00:00+00:00: 1.0
