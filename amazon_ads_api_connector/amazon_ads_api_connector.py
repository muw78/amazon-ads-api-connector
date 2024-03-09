import json
import gzip
import requests
from time import sleep
from .report_types import Report


class AmazonAdsAPIConnector:
    """
    AmazonAdsAPIConnector is a wrapper for the Amazon Advertising API.
    It covers the most important endpoints to manage sponsored products campaigns.
    It also provides methods for authentication, pagination and report creation.
    """

    def __init__(
        self,
        creds: dict,
    ) -> None:
        """
        Args:
            creds (dict): A dictionary containing the credentials for the API including the client_id, client_secret, refresh_token and profile_id.
        """
        self.creds = creds
        self.refresh_access_token()

    def refresh_access_token(
        self,
    ) -> dict:
        """
        Refreshes the access token and the refresh token.

        Returns:
            dict: The response from the API.
        """
        url = "https://api.amazon.co.uk/auth/o2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = f"grant_type=refresh_token&refresh_token={self.creds['refresh_token']}&client_id={self.creds['client_id']}&client_secret={self.creds['client_secret']}"
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )
        result = json.loads(response.text)
        self.creds["access_token"] = result["access_token"]
        self.creds["refresh_token"] = result["refresh_token"]
        return result

    def _get_headers(
        self,
        content_type: str,
    ) -> dict:
        """
        Method to get the headers for the API requests.

        Args:
            content_type (str): The content type of the request.

        Returns:
            dict: The headers for the request.
        """
        return {
            "Amazon-Advertising-API-ClientId": self.creds["client_id"],
            "Authorization": f"Bearer {self.creds['access_token']}",
            "Amazon-Advertising-API-Scope": self.creds["profile_id"],
            "Accept": content_type,
            "Content-Type": content_type,
        }

    def _request_api(
        self,
        method: str,
        url: str,
        headers: dict,
        payload: dict,
    ) -> dict | list:
        """
        Method to make the API requests.

        Args:
            method (str): The method of the request.
            url (str): The url of the request.
            headers (dict): The headers of the request.
            payload (dict): The payload of the request.

        Returns:
            dict | list: The response from the API.
        """
        response = requests.request(
            method,
            url,
            headers=headers,
            data=json.dumps(payload),
        )
        if response.status_code == 401:
            self.refresh_access_token()
            headers = self._get_headers(headers["Content-Type"])
            response = requests.request(
                method,
                url,
                headers=headers,
                data=json.dumps(payload),
            )
        if response.status_code in [200, 207]:
            return json.loads(response.text)
        else:
            raise Exception(response.text)

    def _paginate(
        self,
        method: str,
        url: str,
        headers: dict,
        payload: dict,
        results_name: str,
    ) -> list:
        """
        Method to return lists of results and to paginate in case the results are longer than the maximum page size for the given endpoint.

        Args:
            method (str): The method of the request.
            url (str): The url of the request.
            headers (dict): The headers of the request.
            payload (dict): The payload of the request.
            results_name (str): The name of the results in the response.

        Returns:
            list: The list of results.
        """
        results = []
        while True:
            response = self._request_api(
                method,
                url,
                headers,
                payload,
            )
            if isinstance(response, dict):
                results.extend(response[results_name])
                if "nextToken" in response:
                    payload["nextToken"] = response["nextToken"]
                else:
                    break
        return results

    def list_campaigns(
        self,
        states: list[str] = [
            "ENABLED",
            "PAUSED",
            "ARCHIVED",
        ],
        include_extended_data_fields: bool = False,
        name_contains: list = [""],
    ) -> list:
        """
        Method to list campaigns.

        Args:
            states (list, optional): The states of the campaigns to be listed. Defaults to ["ENABLED", "PAUSED", "ARCHIVED"].
            include_extended_data_fields (bool, optional): Whether to include extended data fields. Defaults to False.
            name_contains (list, optional): The strings the campaign names should contain. Defaults to [""].

        Returns:
            list: The list of campaigns.
        """
        url = "https://advertising-api-eu.amazon.com/sp/campaigns/list"
        payload = {
            "includeExtendedDataFields": include_extended_data_fields,
            "stateFilter": {"include": states},
            "nameFilter": {
                "queryTermMatchType": "BROAD_MATCH",
                "include": name_contains,
            },
        }
        headers = self._get_headers("application/vnd.spCampaign.v3+json")
        return self._paginate("POST", url, headers, payload, "campaigns")

    def create_campaigns(
        self,
        campaigns: list,
    ) -> dict:
        """
        Method to create campaigns.

        Args:
            campaigns (list): The campaigns to be created.
            For more information on the structure of the campaigns, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/Campaigns/operation/CreateSponsoredProductsCampaigns

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/campaigns"
        payload = {
            "campaigns": campaigns,
        }
        headers = self._get_headers("application/vnd.spCampaign.v3+json")
        response = self._request_api(
            "POST",
            url,
            headers,
            payload,
        )
        return response

    def update_campaigns(
        self,
        campaigns: list,
    ) -> dict:
        """
        Method to update campaigns.

        Args:
            campaigns (list): The campaigns to be updated.
            For more information on the structure of the campaigns, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/Campaigns/operation/UpdateSponsoredProductsCampaigns

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/campaigns"
        payload = {
            "campaigns": campaigns,
        }
        headers = self._get_headers("application/vnd.spCampaign.v3+json")
        response = self._request_api(
            "PUT",
            url,
            headers,
            payload,
        )
        return response

    def delete_campaigns(
        self,
        campaign_ids: list,
    ) -> dict:
        """
        Method to delete campaigns.

        Args:
            campaign_ids (list): The ids of the campaigns to be deleted.

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/campaigns/delete"
        payload = {
            "campaignIdFilter": {
                "include": campaign_ids,
            }
        }
        headers = self._get_headers("application/vnd.spCampaign.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def list_ad_groups(
        self,
        campaign_ids: list = [],
        states: list[str] = [
            "ENABLED",
            "PAUSED",
            "ARCHIVED",
        ],
        include_extended_data_fields: bool = False,
        name_contains: list = [""],
    ) -> list:
        """
        Method to list ad groups.

        Args:
            campaign_ids (list, optional): The ids of the campaigns the ad groups belong to. Defaults to [].
            states (list, optional): The states of the ad groups to be listed. Defaults to ["ENABLED", "PAUSED", "ARCHIVED"].
            include_extended_data_fields (bool, optional): Whether to include extended data fields. Defaults to False.
            name_contains (list, optional): The strings the ad group names should contain. Defaults to [""].

        Returns:
            list: The list of ad groups.
        """
        url = "https://advertising-api-eu.amazon.com/sp/adGroups/list"
        payload = {
            "campaignIdFilter": {"include": campaign_ids},
            "stateFilter": {"include": states},
            "includeExtendedDataFields": include_extended_data_fields,
            "nameFilter": {
                "queryTermMatchType": "BROAD_MATCH",
                "include": name_contains,
            },
        }
        headers = self._get_headers("application/vnd.spAdGroup.v3+json")
        return self._paginate("POST", url, headers, payload, "adGroups")

    def create_ad_groups(
        self,
        ad_groups: list,
    ) -> dict:
        """
        Method to create ad groups.

        Args:
            ad_groups (list): The ad groups to be created.
            For more information on the structure of the ad groups, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/AdGroups/operation/CreateSponsoredProductsAdGroups

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/adGroups"
        payload = {
            "adGroups": ad_groups,
        }
        headers = self._get_headers("application/vnd.spAdGroup.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def update_ad_groups(
        self,
        ad_groups: list,
    ) -> dict:
        """
        Method to update ad groups.

        Args:
            ad_groups (list): The ad groups to be updated.
            For more information on the structure of the ad groups, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/AdGroups/operation/UpdateSponsoredProductsAdGroups

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/adGroups"
        payload = {
            "adGroups": ad_groups,
        }
        headers = self._get_headers("application/vnd.spAdGroup.v3+json")
        return self._request_api(
            "PUT",
            url,
            headers,
            payload,
        )

    def delete_ad_groups(
        self,
        ad_group_ids: list,
    ) -> dict:
        """
        Method to delete ad groups.

        Args:
            ad_group_ids (list): The ids of the ad groups to be deleted.

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/adGroups/delete"
        payload = {
            "adGroupIdFilter": {
                "include": ad_group_ids,
            }
        }
        headers = self._get_headers("application/vnd.spAdGroup.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def list_product_ads(
        self,
        campaign_ids: list = [],
        ad_group_ids: list = [],
        states: list = [
            "ENABLED",
            "PAUSED",
            "ARCHIVED",
        ],
        include_extended_data_fields=False,
    ) -> list:
        """
        Method to list product ads.

        Args:
            campaign_ids (list, optional): The ids of the campaigns the product ads belong to. Defaults to [].
            ad_group_ids (list, optional): The ids of the ad groups the product ads belong to. Defaults to [].
            states (list, optional): The states of the product ads to be listed. Defaults to ["ENABLED", "PAUSED", "ARCHIVED"].
            include_extended_data_fields (bool, optional): Whether to include extended data fields. Defaults to False.
        """
        url = "https://advertising-api-eu.amazon.com/sp/productAds/list"
        payload = {
            "campaignIdFilter": {"include": campaign_ids},
            "adGroupIdFilter": {"include": ad_group_ids},
            "stateFilter": {"include": states},
            "includeExtendedDataFields": include_extended_data_fields,
        }
        headers = self._get_headers("application/vnd.spProductAd.v3+json")
        return self._paginate("POST", url, headers, payload, "productAds")

    def create_product_ads(
        self,
        product_ads: list,
    ) -> dict:
        """
        Method to create product ads.

        Args:
            product_ads (list): The product ads to be created.
            For more information on the structure of the product ads, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/ProductAds/operation/CreateSponsoredProductsProductAds

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/productAds"
        payload = {
            "productAds": product_ads,
        }
        headers = self._get_headers("application/vnd.spProductAd.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def update_product_ads(
        self,
        product_ads: list,
    ) -> dict:
        """
        Method to update product ads.

        Args:
            product_ads (list): The product ads to be updated.
            For more information on the structure of the product ads, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/ProductAds/operation/UpdateSponsoredProductsProductAds

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/productAds"
        payload = {
            "productAds": product_ads,
        }
        headers = self._get_headers("application/vnd.spProductAd.v3+json")
        return self._request_api(
            "PUT",
            url,
            headers,
            payload,
        )

    def delete_product_ads(
        self,
        product_ad_ids: list,
    ) -> dict:
        """
        Method to delete product ads.

        Args:
            product_ad_ids (list): The ids of the product ads to be deleted.

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/productAds/delete"
        payload = {
            "adIdFilter": {
                "include": product_ad_ids,
            }
        }
        headers = self._get_headers("application/vnd.spProductAd.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def list_keywords(
        self,
        campaign_ids: list = [],
        ad_group_ids: list = [],
        states=[
            "ENABLED",
            "PAUSED",
            "ARCHIVED",
        ],
        match_types=["BROAD", "EXACT", "PHRASE"],
        include_extended_data_fields=False,
    ) -> list:
        """
        Method to list keywords.

        Args:
            campaign_ids (list, optional): The ids of the campaigns the keywords belong to. Defaults to [].
            ad_group_ids (list, optional): The ids of the ad groups the keywords belong to. Defaults to [].
            states (list, optional): The states of the keywords to be listed. Defaults to ["ENABLED", "PAUSED", "ARCHIVED"].
            match_types (list, optional): The match types of the keywords to be listed. Defaults to ["BROAD", "EXACT", "PHRASE"].
            include_extended_data_fields (bool, optional): Whether to include extended data fields. Defaults to False.

        Returns:
            list: The list of keywords.
        """
        url = "https://advertising-api-eu.amazon.com/sp/keywords/list"
        payload = {
            "campaignIdFilter": {"include": campaign_ids},
            "adGroupIdFilter": {"include": ad_group_ids},
            "stateFilter": {"include": states},
            "matchTypeFilter": match_types,
            "includeExtendedDataFields": include_extended_data_fields,
        }
        headers = self._get_headers("application/vnd.spKeyword.v3+json")
        return self._paginate("POST", url, headers, payload, "keywords")

    def create_keywords(
        self,
        keywords: list,
    ) -> dict:
        """
        Method to create keywords.

        Args:
            keywords (list): The keywords to be created.
            For more information on the structure of the keywords, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/Keywords/operation/CreateSponsoredProductsKeywords

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/keywords"
        payload = {
            "keywords": keywords,
        }
        headers = self._get_headers("application/vnd.spKeyword.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def update_keywords(
        self,
        keywords: list,
    ) -> dict:
        """
        Method to update keywords.

        Args:
            keywords (list): The keywords to be updated.
            For more information on the structure of the keywords, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/Keywords/operation/UpdateSponsoredProductsKeywords

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/keywords"
        payload = {
            "keywords": keywords,
        }
        headers = self._get_headers("application/vnd.spKeyword.v3+json")
        return self._request_api(
            "PUT",
            url,
            headers,
            payload,
        )

    def delete_keywords(
        self,
        keyword_ids: list,
    ) -> dict:
        """
        Method to delete keywords.

        Args:
            keyword_ids (list): The ids of the keywords to be deleted.

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/keywords/delete"
        payload = {
            "keywordIdFilter": {
                "include": keyword_ids,
            }
        }
        headers = self._get_headers("application/vnd.spKeyword.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def list_negative_keywords(
        self,
        campaign_ids: list = [],
        ad_group_ids: list = [],
        states=[
            "ENABLED",
            "PAUSED",
            "ARCHIVED",
        ],
        include_extended_data_fields=False,
    ) -> list:
        """
        Method to list negative keywords.

        Args:
            campaign_ids (list, optional): The ids of the campaigns the negative keywords belong to. Defaults to [].
            ad_group_ids (list, optional): The ids of the ad groups the negative keywords belong to. Defaults to [].
            states (list, optional): The states of the negative keywords to be listed. Defaults to ["ENABLED", "PAUSED", "ARCHIVED"].
            include_extended_data_fields (bool, optional): Whether to include extended data fields. Defaults to False.

        Returns:
            list: The list of negative keywords.
        """
        url = "https://advertising-api-eu.amazon.com/sp/negativeKeywords/list"
        payload = {
            "campaignIdFilter": {"include": campaign_ids},
            "adGroupIdFilter": {"include": ad_group_ids},
            "stateFilter": {"include": states},
            "includeExtendedDataFields": include_extended_data_fields,
        }
        headers = self._get_headers("application/vnd.spNegativeKeyword.v3+json")
        return self._paginate("POST", url, headers, payload, "negativeKeywords")

    def create_negative_keywords(
        self,
        negative_keywords: list,
    ) -> dict:
        """
        Method to create negative keywords.

        Args:
            negative_keywords (list): The negative keywords to be created.
            For more information on the structure of the negative keywords, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/NegativeKeywords/operation/CreateSponsoredProductsNegativeKeywords

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/negativeKeywords"
        payload = {
            "negativeKeywords": negative_keywords,
        }
        headers = self._get_headers("application/vnd.spNegativeKeyword.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def update_negative_keywords(
        self,
        negative_keywords: list,
    ) -> dict:
        """
        Method to update negative keywords.

        Args:
            negative_keywords (list): The negative keywords to be updated.
            For more information on the structure of the negative keywords, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/NegativeKeywords/operation/UpdateSponsoredProductsNegativeKeywords

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/negativeKeywords"
        payload = {
            "negativeKeywords": negative_keywords,
        }
        headers = self._get_headers("application/vnd.spNegativeKeyword.v3+json")
        return self._request_api(
            "PUT",
            url,
            headers,
            payload,
        )

    def delete_negative_keywords(
        self,
        negative_keyword_ids: list,
    ) -> dict:
        """
        Method to delete negative keywords.

        Args:
            negative_keyword_ids (list): The ids of the negative keywords to be deleted.

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/negativeKeywords/delete"
        payload = {
            "keywordIdFilter": {
                "include": negative_keyword_ids,
            }
        }
        headers = self._get_headers("application/vnd.spNegativeKeyword.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def list_targeting_clauses(
        self,
        campaign_ids: list = [],
        ad_group_ids: list = [],
        states=[
            "ENABLED",
            "PAUSED",
            "ARCHIVED",
        ],
        include_extended_data_fields=False,
    ) -> list:
        """
        Method to list targeting clauses.

        Args:
            campaign_ids (list, optional): The ids of the campaigns the targeting clauses belong to. Defaults to [].
            ad_group_ids (list, optional): The ids of the ad groups the targeting clauses belong to. Defaults to [].
            states (list, optional): The states of the targeting clauses to be listed. Defaults to ["ENABLED", "PAUSED", "ARCHIVED"].
            include_extended_data_fields (bool, optional): Whether to include extended data fields. Defaults to False.

        Returns:
            list: The list of targeting clauses.
        """
        url = "https://advertising-api-eu.amazon.com/sp/targets/list"
        payload = {
            "campaignIdFilter": {"include": campaign_ids},
            "adGroupIdFilter": {"include": ad_group_ids},
            "stateFilter": {"include": states},
            "includeExtendedDataFields": include_extended_data_fields,
        }
        headers = self._get_headers("application/vnd.spTargetingClause.v3+json")
        return self._paginate("POST", url, headers, payload, "targetingClauses")

    def create_targeting_clauses(
        self,
        targeting_clauses: list,
    ) -> dict:
        """
        Method to create targeting clauses.

        Args:
            targeting_clauses (list): The targeting clauses to be created.
            For more information on the structure of the targeting clauses, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/TargetingClauses/operation/CreateSponsoredProductsTargetingClauses

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/targets"
        payload = {
            "targetingClauses": targeting_clauses,
        }
        headers = self._get_headers("application/vnd.spTargetingClause.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def update_targeting_clauses(
        self,
        targeting_clauses: list,
    ) -> dict:
        """
        Method to update targeting clauses.

        Args:
            targeting_clauses (list): The targeting clauses to be updated.
            For more information on the structure of the targeting clauses, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/CampaignNegativeTargetingClauses/operation/UpdateSponsoredProductsCampaignNegativeTargetingClauses

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/targets"
        payload = {
            "targetingClauses": targeting_clauses,
        }
        headers = self._get_headers("application/vnd.spTargetingClause.v3+json")
        return self._request_api(
            "PUT",
            url,
            headers,
            payload,
        )

    def delete_targeting_clauses(
        self,
        targeting_clause_ids: list,
    ) -> dict:
        """
        Method to delete targeting clauses.

        Args:
            targeting_clause_ids (list): The ids of the targeting clauses to be deleted.

        Returns:
            dict: The response from the API.
        """
        url = "https://advertising-api-eu.amazon.com/sp/targets/delete"
        payload = {
            "targetIdFilter": {
                "include": targeting_clause_ids,
            }
        }
        headers = self._get_headers("application/vnd.spTargetingClause.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def get_keyword_recommendations(
        self,
        campaign_id: str,
        ad_group_id: str,
        targets,
    ) -> dict:
        """
        Method to get keyword recommendations.

        Args:
            campaign_id (str): The id of the campaign.
            ad_group_id (str): The id of the ad group.
            targets (list): The targets for which to get keyword recommendations.
            For more information on the structure of the targets, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/Keyword-Recommendations/operation/getRankedKeywordRecommendation

        Returns:
            dict: The response from the API.
        """
        url = (
            "https://advertising-api-eu.amazon.com/sp/targets/keywords/recommendations"
        )
        payload = {
            "recommendationType": "KEYWORDS_FOR_ADGROUP",
            "campaignId": campaign_id,
            "adGroupId": ad_group_id,
            "targets": targets,
            "maxRecommendations": 0,
        }
        headers = self._get_headers("application/vnd.spkeywordsrecommendation.v4+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def get_bid_recommendations_for_ad_groups(
        self,
        campaign_id: str,
        ad_group_ids: list,
        targeting_expressions: list = [
            {"type": "CLOSE_MATCH"},
            {"type": "LOOSE_MATCH"},
            {"type": "SUBSTITUTES"},
            {"type": "COMPLEMENTS"},
        ],
    ) -> dict:
        """
        Method to get bid recommendations for ad groups. It supports keyword, auto and product targets.
        The targeting expressions of the method default to recommendations for auto campaigns.

        Args:
            campaign_id (str): The id of the campaign.
            ad_group_ids (list): The ids of the ad groups.
            targeting_expressions (list, optional): The targeting expressions for which to get bid recommendations. Defaults to [{"type": "CLOSE_MATCH"}, {"type": "LOOSE_MATCH"}, {"type": "SUBSTITUTES"}, {"type": "COMPLEMENTS"}].
            For more information on the structure of the targeting expressions, see
            https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod#tag/Theme-based-bid-recommendations/operation/GetThemeBasedBidRecommendationForAdGroup_v1
        """
        url = "https://advertising-api-eu.amazon.com/sp/targets/bid/recommendations"
        payload = {
            "targetingExpressions": targeting_expressions,
            "campaignId": campaign_id,
            "recommendationType": "BIDS_FOR_EXISTING_AD_GROUP",
            "adGroupId": ad_group_ids,
        }
        headers = self._get_headers(
            "application/vnd.spthemebasedbidrecommendation.v4+json"
        )
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def create_report(
        self,
        report: Report,
    ) -> dict:
        """
        Method to create a report.

        Args:
            report (Report): The report to be created as an object of one of the classes in report_types.py.
            For more information on the structure of the reports, see
            https://advertising.amazon.com/API/docs/en-us/offline-report-prod-3p
            and
            https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types#tag/Asynchronous-Reports/operation/createAsyncReport

        Returns:
            dict: The response from the API. It contains the report id.
        """
        url = "https://advertising-api-eu.amazon.com/reporting/reports"
        payload = {
            "name": "Report",
            "startDate": report.start_date,
            "endDate": report.end_date,
            "configuration": {
                "adProduct": "SPONSORED_PRODUCTS",
                "groupBy": report.group_by,
                "columns": report.metrics,
                "reportTypeId": report.report_type_id,
                "timeUnit": "SUMMARY",
                "format": "GZIP_JSON",
            },
        }
        headers = self._get_headers("application/vnd.createasyncreportrequest.v3+json")
        return self._request_api(
            "POST",
            url,
            headers,
            payload,
        )

    def get_report(
        self,
        report_request: dict,
    ) -> dict:
        """
        Method to retrieve a report.

        Args:
            report_request (dict): The report request containing the report id.

        Returns:
            dict: The report.
        """
        url = f"https://advertising-api-eu.amazon.com/reporting/reports/{report_request['reportId']}"
        headers = self._get_headers("application/vnd.advertisingReport+json")
        while True:
            response = json.loads(requests.request("GET", url, headers=headers).text)
            if response["status"] == "COMPLETED":
                report = requests.request("GET", response["url"]).content
                return json.loads(gzip.decompress(report))
            sleep(5)
