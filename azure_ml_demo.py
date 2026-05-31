import urllib.request
import urllib.error
import json

url = "http://8aaea4e1-dd4d-448d-b0ae-aae343ef6656.southeastasia.azurecontainer.io/score"

api_key = "HnTgdd5RbskKM9LWAhxjofCyfyGjqKHz"

discount_applied = float(input("Enter discount applied: "))
revenue = float(input("Enter revenue: "))
clicks = int(input("Enter clicks: "))
impressions = int(input("Enter impressions: "))
conversion_rate = float(input("Enter conversion rate: "))
ad_ctr = float(input("Enter ad CTR: "))
ad_cpc = float(input("Enter ad CPC: "))
ad_spend = float(input("Enter ad spend: "))
price_per_unit = float(input("Enter price per unit: "))
year = int(input("Enter year: "))
month = int(input("Enter month: "))
day = int(input("Enter day: "))
day_of_week = int(input("Enter day of week: "))

data = {
    "Inputs": {
        "WebServiceInput0": [
            {
                "units_sold": 0,
                "discount_applied": discount_applied,
                "revenue": revenue,
                "clicks": clicks,
                "impressions": impressions,
                "conversion_rate": conversion_rate,
                "ad_ctr": ad_ctr,
                "ad_cpc": ad_cpc,
                "ad_spend": ad_spend,
                "price_per_unit": price_per_unit,
                "year": year,
                "month": month,
                "day": day,
                "day_of_week": day_of_week
            }
        ]
    }
}

body = json.dumps(data).encode("utf-8")

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer " + api_key
}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode("utf-8"))

    prediction = result["Results"]["WebServiceOutput0"][0]["Scored Labels"]

    print("\nPredicted Units Sold:", round(float(prediction), 2))

except urllib.error.HTTPError as error:
    print("Status Code:", error.code)
    print(error.read().decode("utf8", "ignore"))

except Exception as e:
    print("Error:", e)