class Report:
    """
    Base class for all report types.
    """

    def __init__(
        self,
        start_date: str,
        end_date: str,
        report_type_id: str,
        metrics: list,
        group_by: list = [],
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.report_type_id = report_type_id
        self.metrics = metrics
        self.group_by = group_by


class CampaignsReport(Report):
    """
    This class contains a basic configuration for the campaign report.
    It can be used to create a report via the AmazonAdvertisingApi.create_report() method.
    Individual attributes can be adjusted as required before passing the object to the method.
    For more information on the attributes, see the Amazon Advertising API documentation:
    https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types#campaign-reports

    Args:
        start_date (str): Start date of the report
        end_date (str): End date of the report
        group_by (list, optional): Group by columns. Defaults to ["campaign"].
    """

    def __init__(self, start_date: str, end_date: str, group_by: list = ["campaign"]):
        self.start_date = start_date
        self.end_date = end_date
        self.report_type_id = "spCampaigns"
        self.group_by = group_by
        self.metrics = [
            "impressions",
            "clicks",
            "cost",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
            "purchasesSameSku1d",
            "purchasesSameSku7d",
            "purchasesSameSku14d",
            "purchasesSameSku30d",
            "unitsSoldClicks1d",
            "unitsSoldClicks7d",
            "unitsSoldClicks14d",
            "unitsSoldClicks30d",
            "sales1d",
            "sales7d",
            "sales14d",
            "sales30d",
            "attributedSalesSameSku1d",
            "attributedSalesSameSku7d",
            "attributedSalesSameSku14d",
            "attributedSalesSameSku30d",
            "unitsSoldSameSku1d",
            "unitsSoldSameSku7d",
            "unitsSoldSameSku14d",
            "unitsSoldSameSku30d",
            "kindleEditionNormalizedPagesRead14d",
            "kindleEditionNormalizedPagesRoyalties14d",
            "startDate",
            "endDate",
            "campaignBiddingStrategy",
            "costPerClick",
            "clickThroughRate",
            "spend",
        ]
        if "campaign" in self.group_by:
            self.metrics.extend(
                [
                    "campaignName",
                    "campaignId",
                    "campaignStatus",
                    "campaignBudgetAmount",
                    "campaignBudgetType",
                    "campaignRuleBasedBudgetAmount",
                    "campaignApplicableBudgetRuleId",
                    "campaignApplicableBudgetRuleName",
                    "campaignBudgetCurrencyCode",
                    "topOfSearchImpressionShare",
                ]
            )
        if "adGroup" in self.group_by:
            self.metrics.extend(["adGroupName", "adGroupId", "adStatus"])


class TargetingReport(Report):
    """
    This class contains a basic configuration for the targeting report.
    It can be used to create a report via the AmazonAdvertisingApi.create_report() method.
    Individual attributes can be adjusted as required before passing the object to the method.
    For more information on the attributes, see the Amazon Advertising API documentation:
    https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types#targeting-reports

    Args:
        start_date (str): Start date of the report
        end_date (str): End date of the report
        group_by (list, optional): Group by columns. Defaults to ["targeting"].
    """

    def __init__(self, start_date: str, end_date: str, group_by: list = ["targeting"]):
        self.start_date = start_date
        self.end_date = end_date
        self.report_type_id = "spTargeting"
        self.group_by = group_by
        self.metrics = [
            "impressions",
            "clicks",
            "costPerClick",
            "clickThroughRate",
            "cost",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
            "purchasesSameSku1d",
            "purchasesSameSku7d",
            "purchasesSameSku14d",
            "purchasesSameSku30d",
            "unitsSoldClicks1d",
            "unitsSoldClicks7d",
            "unitsSoldClicks14d",
            "unitsSoldClicks30d",
            "sales1d",
            "sales7d",
            "sales14d",
            "sales30d",
            "attributedSalesSameSku1d",
            "attributedSalesSameSku7d",
            "attributedSalesSameSku14d",
            "attributedSalesSameSku30d",
            "unitsSoldSameSku1d",
            "unitsSoldSameSku7d",
            "unitsSoldSameSku14d",
            "unitsSoldSameSku30d",
            "kindleEditionNormalizedPagesRead14d",
            "kindleEditionNormalizedPagesRoyalties14d",
            "salesOtherSku7d",
            "unitsSoldOtherSku7d",
            "acosClicks7d",
            "acosClicks14d",
            "roasClicks7d",
            "roasClicks14d",
            "keywordId",
            "keyword",
            "campaignBudgetCurrencyCode",
            "startDate",
            "endDate",
            "portfolioId",
            "campaignName",
            "campaignId",
            "campaignBudgetType",
            "campaignBudgetAmount",
            "campaignStatus",
            "keywordBid",
            "adGroupName",
            "adGroupId",
            "keywordType",
            "matchType",
            "targeting",
            "topOfSearchImpressionShare",
            "adKeywordStatus",
        ]


class SearchTermReport(Report):
    """
    This class contains a basic configuration for the search term report.
    It can be used to create a report via the AmazonAdvertisingApi.create_report() method.
    Individual attributes can be adjusted as required before passing the object to the method.
    For more information on the attributes, see the Amazon Advertising API documentation:
    https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types#search-term-reports

    Args:
        start_date (str): Start date of the report
        end_date (str): End date of the report
        group_by (list, optional): Group by columns. Defaults to ["searchTerm"].
    """

    def __init__(self, start_date: str, end_date: str, group_by: list = ["searchTerm"]):
        self.start_date = start_date
        self.end_date = end_date
        self.report_type_id = "spSearchTerm"
        self.group_by = group_by
        self.metrics = [
            "impressions",
            "clicks",
            "costPerClick",
            "clickThroughRate",
            "cost",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
            "purchasesSameSku1d",
            "purchasesSameSku7d",
            "purchasesSameSku14d",
            "purchasesSameSku30d",
            "unitsSoldClicks1d",
            "unitsSoldClicks7d",
            "unitsSoldClicks14d",
            "unitsSoldClicks30d",
            "sales1d",
            "sales7d",
            "sales14d",
            "sales30d",
            "attributedSalesSameSku1d",
            "attributedSalesSameSku7d",
            "attributedSalesSameSku14d",
            "attributedSalesSameSku30d",
            "unitsSoldSameSku1d",
            "unitsSoldSameSku7d",
            "unitsSoldSameSku14d",
            "unitsSoldSameSku30d",
            "kindleEditionNormalizedPagesRead14d",
            "kindleEditionNormalizedPagesRoyalties14d",
            "salesOtherSku7d",
            "unitsSoldOtherSku7d",
            "acosClicks7d",
            "acosClicks14d",
            "roasClicks7d",
            "roasClicks14d",
            "keywordId",
            "keyword",
            "campaignBudgetCurrencyCode",
            "startDate",
            "endDate",
            "portfolioId",
            "searchTerm",
            "campaignName",
            "campaignId",
            "campaignBudgetType",
            "campaignBudgetAmount",
            "campaignStatus",
            "keywordBid",
            "adGroupName",
            "adGroupId",
            "keywordType",
            "matchType",
            "targeting",
            "adKeywordStatus",
        ]


class AdvertisedProductReports(Report):
    """
    This class contains a basic configuration for the advertised product report.
    It can be used to create a report via the AmazonAdvertisingApi.create_report() method.
    Individual attributes can be adjusted as required before passing the object to the method.
    For more information on the attributes, see the Amazon Advertising API documentation:
    https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types#advertised-product-reports

    Args:
        start_date (str): Start date of the report
        end_date (str): End date of the report
        group_by (list, optional): Group by columns. Defaults to ["advertiser"].
    """

    def __init__(self, start_date: str, end_date: str, group_by: list = ["advertiser"]):
        self.start_date = start_date
        self.end_date = end_date
        self.report_type_id = "spAdvertisedProduct"
        self.group_by = group_by
        self.metrics = [
            "startDate",
            "endDate",
            "campaignName",
            "campaignId",
            "adGroupName",
            "adGroupId",
            "adId",
            "portfolioId",
            "impressions",
            "clicks",
            "costPerClick",
            "clickThroughRate",
            "cost",
            "spend",
            "campaignBudgetCurrencyCode",
            "campaignBudgetAmount",
            "campaignBudgetType",
            "campaignStatus",
            "advertisedAsin",
            "advertisedSku",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
            "purchasesSameSku1d",
            "purchasesSameSku7d",
            "purchasesSameSku14d",
            "purchasesSameSku30d",
            "unitsSoldClicks1d",
            "unitsSoldClicks7d",
            "unitsSoldClicks14d",
            "unitsSoldClicks30d",
            "sales1d",
            "sales7d",
            "sales14d",
            "sales30d",
            "attributedSalesSameSku1d",
            "attributedSalesSameSku7d",
            "attributedSalesSameSku14d",
            "attributedSalesSameSku30d",
            "salesOtherSku7d",
            "unitsSoldSameSku1d",
            "unitsSoldSameSku7d",
            "unitsSoldSameSku14d",
            "unitsSoldSameSku30d",
            "unitsSoldOtherSku7d",
            "kindleEditionNormalizedPagesRead14d",
            "kindleEditionNormalizedPagesRoyalties14d",
            "acosClicks7d",
            "acosClicks14d",
            "roasClicks7d",
            "roasClicks14d",
        ]


class PurchasedProductReport(Report):
    """
    This class contains a basic configuration for the purchased product report.
    It can be used to create a report via the AmazonAdvertisingApi.create_report() method.
    Individual attributes can be adjusted as required before passing the object to the method.
    For more information on the attributes, see the Amazon Advertising API documentation:
    https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types#purchased-product-reports

    Args:
        start_date (str): Start date of the report
        end_date (str): End date of the report
        group_by (list, optional): Group by columns. Defaults to ["asin"].
    """

    def __init__(self, start_date: str, end_date: str, group_by: list = ["asin"]):
        self.start_date = start_date
        self.end_date = end_date
        self.report_type_id = "spPurchasedProduct"
        self.group_by = group_by
        self.metrics = [
            "startDate",
            "endDate",
            "portfolioId",
            "campaignName",
            "campaignId",
            "adGroupName",
            "adGroupId",
            "keywordId",
            "keyword",
            "keywordType",
            "advertisedAsin",
            "purchasedAsin",
            "advertisedSku",
            "campaignBudgetCurrencyCode",
            "matchType",
            "unitsSoldClicks1d",
            "unitsSoldClicks7d",
            "unitsSoldClicks14d",
            "unitsSoldClicks30d",
            "sales1d",
            "sales7d",
            "sales14d",
            "sales30d",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
            "unitsSoldOtherSku1d",
            "unitsSoldOtherSku7d",
            "unitsSoldOtherSku14d",
            "unitsSoldOtherSku30d",
            "salesOtherSku1d",
            "salesOtherSku7d",
            "salesOtherSku14d",
            "salesOtherSku30d",
            "purchasesOtherSku1d",
            "purchasesOtherSku7d",
            "purchasesOtherSku14d",
            "purchasesOtherSku30d",
            "kindleEditionNormalizedPagesRead14d",
            "kindleEditionNormalizedPagesRoyalties14d",
        ]
