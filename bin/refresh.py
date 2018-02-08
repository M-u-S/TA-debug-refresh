#!/opt/splunk/bin/python
# Copyright (C) 2014 MuS
# http://answers.splunk.com/users/2122/mus

# enable / disable logger debug output
myDebug = 'no'

# Changelog
# 18 December 2016 - tested on Splunk 6.5.1
# 19 December 2016 - added logging to splunkd.log / sorting of the result

# import some Python moduls
import splunk
import sys
import os
import splunk.Intersplunk
import re
import logging
import collections
import splunk.rest as rest


# enable debug logging to splunkd.log
def setup_logging(n):
    logger = logging.getLogger(n)  # Root-level logger
    logger.setLevel(logging.DEBUG)
    SPLUNK_HOME = os.environ['SPLUNK_HOME']
    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
    LOGGING_STANZA_NAME = 'python'
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FORMAT = '%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s'
    splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, 'splunkd.log'),
                                                              mode='a')
    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(splunk_log_handler)
    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
    return logger


# start the logger only if needed
if myDebug == 'yes':
    logger = setup_logging('logger started ...')

# starting the main
if myDebug == 'yes':
    logger.debug('starting the main task ...')

# getting the sessionKey, owner, namespace
results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
results = []  # we don't care about incoming results
if myDebug == 'yes': logger.debug('setting: %s ' % settings)
sessionKey = settings.get('sessionKey', None)  # getting session key
if myDebug == 'yes': logger.debug('using sessionKey: %s ' % sessionKey)
owner = settings.get('owner', None)  # getting user / owner
if myDebug == 'yes': logger.debug('using owner: %s ' % owner)
namespace = settings.get('namespace', None)  # getting namespace
if myDebug == 'yes': logger.debug('using namespace: %s ' % namespace)

# setting up empty output list
myList = []

# get rest response and content
response, content = rest.simpleRequest('/servicesNS/-/search/admin', sessionKey=sessionKey, method='GET')

# getting all the _reload links form the response content
reloadLinks = []  # set empty list
for line in content.split('\n'):  # loop throught the content
    if myDebug == 'yes': logger.debug('line: %s ' % line)
    if '_reload' in line:  # _reload link found
        reloadLink = re.findall(r'href\=\"(.+?)\"', line)  # getting the links
        if myDebug == 'yes': logger.debug('reloadLink: %s ' % reloadLink)
        if not reloadLink:  # if no link was found
            if myDebug == 'yes':
                logger.debug('line did not match ...')
        for name in reloadLink:  # add only capable endpoints / take from debug.py
            if myDebug == 'yes':
                logger.debug('name: %s' % name)
            if myDebug == 'yes':
                logger.debug('checking auth-service: ...')
            if 'auth-services' in name:  # refreshing auth causes logout, no reload here!
                if myDebug == 'yes':
                    logger.debug('found auth-service: stepping forward ...')
                continue
            if myDebug == 'yes':
                logger.debug('checking windows: ...')
            if sys.platform == 'win32' and name == 'fifo':
                # splunkd never loads FIFO on windows, but advertises it anyway
                if myDebug == 'yes':
                    logger.debug('found windows stuff: stepping forward ...')
                continue
            if myDebug == 'yes':
                logger.debug('appending final links ...')
            reloadLinks.append(name)  # appending relaod link to list

if myDebug == 'yes':
    logger.debug('final reloadLinks: %s' % reloadLinks)

# reloading the endpoints now
if myDebug == 'yes':
    logger.debug('reloading the endpoints now ...')
for target in reloadLinks:  # looping through the reload links
    endpointresult = {}  # set empty result dict
    if myDebug == 'yes':
        logger.debug('reloading the %s endpoints now ...' % target)
    # get rest response and content
    response, content = rest.simpleRequest(target, sessionKey=sessionKey, method='POST')
    endpointresult['endpoint'] = target  # set result endpoint
    endpointresult['status'] = response['status']  # set endpoint reload status
    if myDebug == 'yes':
        logger.debug('endpointresult: %s' % endpointresult)
    od = collections.OrderedDict(sorted(endpointresult.items()))  # sort the list
    myList.append(od)  # append the ordered results to the list

if myDebug == 'yes':
    logger.debug('done with the work ...')
if myDebug == 'yes':
    logger.debug('this is myList: %s' % myList)

if myDebug == 'yes':
    logger.debug('output the result to splunk> ...')
splunk.Intersplunk.outputResults(myList)  # output the result to splunk
