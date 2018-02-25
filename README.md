## Usage ##
This is a Add-on for Splunk to provide a custom search command called 'refresh'
to reload most of the Splunk config endpoints.

Simply call `| refresh` in the search bar to reload the endpoints or enable the
saved search to have this process scheduled.

## Installation ##
- Install as any other Splunk App
- If needed modify and enable the included saved search called 'Debug Refresh'.

## Debug ##
If needed you can enabled debugging to splunkd.log in the script refresh.py by
setting myDebug='yes' on line 6

**Support**

This is an open source project, no support provided, but you can ask questions
on answers.splunk.com and I will most likely answer it.
Github repository: https://github.com/M-u-S/SA-debug-refresh
