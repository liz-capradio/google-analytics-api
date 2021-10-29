"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta, date
import time
import csv
import json

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'credentials.json'


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics, viewid, segmentid, startdate, enddate):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """

    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': viewid,
                    'dateRanges': [{'startDate': startdate, 'endDate': enddate}],
                    'metrics': [{'expression': 'ga:users'}],
                    'dimensions': [{'name': 'ga:country', 'name': 'ga:segment'}],
                    'segments': [{'segmentId': 'gaid::'+segmentid}]
                }]
        }
    ).execute()


def print_response(response):
    """Parses, prints and returns the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get(
            'metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ', dimension)

            for i, values in enumerate(dateRangeValues):
                print('Date range:', str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print(metricHeader.get('name') + ':', value)
                    return value


def main(config):
    analytics = initialize_analyticsreporting()
    viewid = config['viewid']
    segmentid = config['segmentid']
    startdate = config['startdate']
    enddate = config['enddate']
    errorCount = 0
    results = []

    # set up date parameters and count weeks
    sd = datetime.strptime(startdate, '%Y-%m-%d')
    ed = datetime.strptime(enddate, '%Y-%m-%d')
    days = abs(sd-ed).days
    numWeeks = days//7

    # set starting date parameters (end date here is now the end of the week)
    td = timedelta(6)
    sd = datetime.strptime(startdate, '%Y-%m-%d')
    ed = datetime.strptime(startdate, '%Y-%m-%d') + td
    startdate = datetime.strftime(sd, '%Y-%m-%d')
    enddate = datetime.strftime(ed, '%Y-%m-%d')

    # column names
    results.append(['startdate', 'enddate', 'users-'+segmentid])
    for i in range(0, numWeeks):
        print(str(i) + ": " + startdate + " - " + enddate)

        try:
            response = get_report(
                analytics, viewid, segmentid, startdate, enddate)
            value = print_response(response)
            results.append([startdate, enddate, value])
        except:
            # Whoops it wasn't a 200
            errorCount += 1
            results.append([startdate, enddate, 'ERROR'])
            print("Error with API request.")

        # add seven days to start next loop
        td = timedelta(7)
        sd = datetime.strptime(startdate, '%Y-%m-%d') + td
        ed = datetime.strptime(enddate, '%Y-%m-%d') + td
        startdate = datetime.strftime(sd, '%Y-%m-%d')
        enddate = datetime.strftime(ed, '%Y-%m-%d')

    print("Number of errors from API: "+str(errorCount))
    with open("output.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter=",")
        for r in results:
            writer.writerow(r)


if __name__ == '__main__':
    with open('setup.json') as json_file:
        data = json.load(json_file)
    main(data)
