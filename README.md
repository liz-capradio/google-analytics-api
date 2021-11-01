# GA Segment data from Google API

This code is intended to collect the number of users from one segment at a time. Input will consist of start date, end date, view ID and segment ID. It will output to output.csv with three columns: start date, end date, number of users in segment.

Example:
```
{
"viewid":"12345678",
"segmentid": "uNiQuE-IdEnTiFieR",
"startdate": "2015-12-27", // this should be on the day of the week you want your data to look for
"enddate": "2021-10-28" // this will be used to calculate the number of weeks to pull, so it won't stop exactly on this date unless you did the math right
}
```

## Set up Google Analytics

1. Select which View you want to create a segment for and note it's ID. [This](https://ga-dev-tools.web.app/account-explorer/) helps you learn more about your environment make up if you need it.
1. Import segment ([NPR Station Loyalty Guide](https://docs.google.com/document/d/1ddHJrjkSb1nRaPzlrnBjvt2AkIt5R5Np_YeazT9JP7Q/edit)) or create one in Google Analytics. (You can use any [default segment](https://stuifbergen.com/2018/02/google-analytics-api-built-in-segments-the-complete-list/) and skip this step.)
1. Share segment to the view (Go to Admin > View > Segments - find your segment > Edit > Top Right and make sure you horizontal scroll past the whitespace to find where to 'Change', select option to allow collaborators in view to use segment).
1. Find segment ID by adding it to a custom report, it will be in the URL following '/\_.useg=user'. Remove all other segments to make it clear. You can use this report to double check the numbers from the output are correct.

## Set up Code

1. Follow the instructions on how to set up a service account: https://developers.google.com/analytics/devguides/reporting/core/v3/quickstart/service-py?hl=en
1. Add the credentials.json to the root.
1. Create a 'setup.json' file with the details about your segment and the dates (format: "2021-10-28") you want to collect data for, keep in mind that the code will increment 7 days from the start date UNTIL the end date. (Change name of 'setup copy.json' to use)
