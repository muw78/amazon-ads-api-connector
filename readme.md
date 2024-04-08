# Amazon Ads API Connector

A simple Python wrapper for the <a href="https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod">latest version of the Amazon Ads API for Sponsored Products campaign management</a>.

This module covers the key endpoints for managing Sponsored Products campaigns. This includes methods for authentication, pagination and report generation. It features keyword and negative keyword targeting, as well as product ASIN targeting and auto campaigns. 

Please note that this module does not yet support Sponsored Brands and Sponsored Display campaigns.

## Installation

Amazon Ads API Connector is available on PyPI:

```bash
pip install amazon-ads-api-connector
```

## Getting started

The primary class of the module is `AmazonAdsAPIConnector`. This class provides methods to create, list, update and delete 
- campaigns, 
- ad groups, 
- product ads, 
- keywords, 
- negative keywords, and
- targeting clauses (ASIN targeting).

It furthermore provides methods to get `keyword recommendations`, which include bid recommendations for keyword targets, as well as `bid recommendations for ad groups`, which include bid recommendations for auto campaigns.

And lastly, it provides also methods to request and retrieve reports via the API.

To create an instance of the `AmazonAdsAPIConnector`, you need to pass your Amazon Ads API credentials as a dictionary. The dictionary must contain the following keys:

- `refresh_token`
- `client_id`
- `client_secret`
- `profile_id`

Upon initialization, the AmazonAdsAPIConnector object will create a new access token. This access token will be valid for 60 minutes, however, the object automatically requests a new access token in case it has expired when trying to make a new request.

For more information about the Amazon Ads API, please visit the [official documentation](https://advertising.amazon.com/API/docs/en-us/get-started/how-to-use-api).

## Examples
### Import the library
```python
from amazon_ads_api_connector import AmazonAdsAPIConnector
```
### Create an instance
```python
api = AmazonAdsAPIConnector(
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
Please note that all create and update methods expect a list of dictionaries as their only argument. This reflects the fact that the Amazon Ads API allows to create or update multiple objects at once. To ensure the greatest possible flexibility, the structure of the list and the dictionaries corresponds to the structure specified by the API and described in the API documentation. For more information about the structure of the lists and dictionaries, as well for information on data limits per request, please visit the [official documentation](https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod).

### Request and retrieve a report

The module contains classes which represent basic configurations of the available report types:

- `CampaignsReport`
- `TargetingReport`
- `SearchTermReport`
- `AdvertisedProductReports`
- `PurchasedProductReport`

For more information about the report types, please visit the [official documentation](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types).

To request a report you need to pass an instance of one of these classes to the `create_report` method of the `AmazonAdsAPIConnector` class. To customize the report, change the properties of the class instance before passing it to the `create_report` method.

```python
from amazon_ads_api_connector import SearchTermReport

report_configuration = SearchTermReport("2023-10-01", ◊"2023-10-07")

res = api.create_report(report_configuration)
report = api.get_report(res)
```
Please note that report gerneration is asynchronous. The `create_report` method returns a dictionary containing the report ID. The `get_report` takes this dictionary as an argument and returns the report once it is completed and available. The completion of a report usually takes a few minutes and can take up to 3 hours.

## Dependencies

This module depends on the `requests` library, which is not included in the Python standard library, but will be installed automatically when you install the `amazon-ads-api-connector` package.

## Disclaimer

This module is not affiliated with Amazon in any way. It is an independent project that aims to provide a simple and easy-to-use interface to the Amazon Ads API for Sponsored Products campaign management.