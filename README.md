## Usage ##
This is a Add-on for Splunk to provide a custom search command called 'refresh'
to reload most of the Splunk config endpoints.

It does not reload `admin/cooked` and `admin/auth-services` be default.

Simply call `| refresh` in the search bar to reload the endpoints. Use `| refresh entity=all` to also reload the splunktcp cooked REST endpoint (can result in data loss!)

Or specify an entity to be reloaded `| refresh entity=foo`

To get a list of all entities that can be reloaded use `| refresh entity=list`

## Installation ##
- Install as any other Splunk App

## Debug ##
If needed you can enabled debugging to splunkd.log in the script `refresh.py` by
setting `myDebug='yes'` on line 6

**Support**

This is an open source project, no support provided, but you can ask questions
on answers.splunk.com and I will most likely answer it.
Github repository: https://github.com/M-u-S/TA-debug-refresh

This TA has passed appinspect with the cloud tag, the result output is in the README directory.

Running Splunk on Windows? Good Luck, not my problem.


## Version ##
`18. August 2018 : 2.3.0 - added entity option`
`12. February 2022 : 3.0.0 - Python 3`
`17. August 2022 : 3.0.1 - Minor changes to outputs`
