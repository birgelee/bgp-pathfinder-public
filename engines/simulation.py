#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import datetime
import time
import random
import os
import sys

fileDirectory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(fileDirectory + "/../../topology-simulator")
print(fileDirectory)
print(fileDirectory + "/../../topology-simulator")
import simulate

simulate.init()

def get_current_human_time():
	value = datetime.datetime.fromtimestamp(time.time())
	return value.astimezone(datetime.timezone.utc).strftime('UTC %Y-%m-%d %H:%M:%S')

currentAnnouncements = {}
# announcementList is of the format [("CIDR-format-prefix", ["BGP:community", ...], ["poison ASN", ...]), ...]
def make_announcement(node, announcementList):
	global currentAnnouncements
	if announcementList == []:
		if node in currentAnnouncements:
			del currentAnnouncements[node]
	else:
		currentAnnouncements[node] = announcementList
		print(announcementList)


def get_path(node, prefix):
	origins = [node for node in currentAnnouncements if prefix in [prefixCommunityPoison[0] for prefixCommunityPoison in currentAnnouncements[node]]]
	if len(origins) > 1:
		print("Multiple origins for simulated prefixes not currently supported")
		raise NotImplementedError()
	if len(origins) == 0:
		return "" # No route is Empty string in above logic
	annoncementSetForOrigin = currentAnnouncements[origins[0]]
	announcementForPrefixForOrigin = [ao for ao in annoncementSetForOrigin if ao[0] == prefix][0]
	attachedCommunities = announcementForPrefixForOrigin[1]
	simulate.clearPrefixPolicies(prefix)
	policiesToAdd = []
	for community in attachedCommunities:
		splitCommunity = community.split(":")
		Y = splitCommunity[0]
		X = splitCommunity[1]
		#policiesToAdd.append(f"{Y}:NO_EXPORT@{X}>{prefix}")
		policiesToAdd.append(f"{Y}:NO_EXPORT_AT_PEER_OR_PROVIDER@{X}>{prefix}")
	simulate.addPolicies(policiesToAdd)
	res = simulate.simulate(prefix, origins, [node])
	
	retVal = res[node][2] if node in res else ""
	simulate.clearPrefixPolicies(prefix)
	return retVal



