# Amazon Ads API Connector

A simple Python wrapper for the <a href="https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod">latest version of the Amazon Ads API for Sponsored Products campaign management</a>.

This library covers the key endpoints for managing Sponsored Products campaigns. This includes methods for authentication, pagination and report generation.

Please note that this library does not yet support Sponsored Brands and Sponsored Display campaigns. It also does not yet feature product and category targeting.

## Getting started

The primary class of the library is `AmazonAdsApiConnector`, which is defined in the file `amazon_ads_api_connector.py`. 

This class provides methods to create, list, update and delete 
- campaigns, 
- ad groups, 
- product ads, 
- keywords, and 
- negative keywords. 

It furthermore provides methods to request and retrieve reports via the API.

To create an instance of the `AmazonAdsApiConnector`, you need to pass your Amazon Advertising API credentials as a dictionary. The dictionary must contain the following keys:

- `refresh_token`
- `client_id`
- `client_secret`
- `profile_id`

Upon initialization, the AmazonAdsApiConnector object will create a new access token. The access token will be valid for 60 minutes, however, the object automatically requests a new access token in case it has expired when trying to make a new request.

For more information about the Amazon Advertising API, please visit the [official documentation](https://advertising.amazon.com/API/docs/en-us/get-started/how-to-use-api).
## Report Types
The file `report_types.py` contains classes with basic configurations of the available report types. For more information about the report types, please visit the [official documentation](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types).
## Examples
### Import the library
```python
from amazon_ads_api_connector import AmazonAdsApiConnector
```
### Create an instance
```python
api = AmazonAdsApiConnector(
    {
        "refresh_token": "your_refresh_token",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "profile_id": "your_profile_id",
    }
)
```
### List campaigns
```python
campaigns = api.list_campaigns()
```
### Create campaigns
```python
api.create_campaign(
    campaigns=[
        {
            "name": "My Campaign",
            "targetingType": "MANUAL",
            "state": "ENABLED",
            "dynamicBidding": {
                "strategy": "LEGACY_FOR_SALES",
            },
            "bugdget": {
                "budgetType": "DAILY",
                "budget": 0,
            },
        },
    ]
)
```
Please note that all create and update methods expect a list of dictionaries as their only argument. This is because the API allows to create or update multiple objects at once. To ensure the greatest possible flexibility, the structure of the list and the dictionaries corresponds to the structure specified by the API and described in the API documentation.

### Request and retrieve a report
```python
from report_types import SponsoredProductsReport

res = api.create_report(SearchTermReport("2023-10-01", "2023-10-07"))
report = api.get_report(res)
```
Please note that report gerneration is asynchronous. The `create_report` method returns a dictionary containing the report ID. The `get_report` takes this dictionary as an argument and returns the report once it is completed and available. The completion of a report usually takes a few minutes and can take up to 3 hours.