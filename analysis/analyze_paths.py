#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import matplotlib.pyplot as plt
import numpy as np


def parse_args():
	parser = argparse.ArgumentParser()
	# This is a CAIDA AS topology.
	parser.add_argument("-p", "--paths_file",
	                    default="../output/paths.txt")
	return parser.parse_args()


def replace0sWith1s(numberList):
	return [1 if n == 0 else n for n in numberList]

def main(args):
	pathsList = []
	for line in open(args.paths_file):
		sline = line.strip()
		if sline == "":
			continue
		jline = json.loads(sline)
		pathsList.append(jline['paths']) # paths is a list of pathsCommunitiesPoisonsTuples


	tier1SetWikipedia = {"7018", "3320", "3257", "6830", "3356", "3549", "2914", "5511", "3491", "1239", "6453", "6762", "1299", "12956", "701", "6461"}
	pathsWithoutDirectTier1UpstreamsInThem = [[pathsCommunitiesPoisonsTuple for pathsCommunitiesPoisonsTuple in pathsCommunitiesPoisonsLists if pathsCommunitiesPoisonsTuple[0][-2] not in tier1SetWikipedia] for pathsCommunitiesPoisonsLists in pathsList]
	pathCountsWithoutDirectTier1Upstreams = [len(p) for p in pathsWithoutDirectTier1UpstreamsInThem]
	pathCountsWithoutDirectTier1UpstreamsOnlyVultrCommunities = [len([pathsCommunitiesPoisonsTuple for pathsCommunitiesPoisonsTuple in pathsCommunitiesPoisonsLists if all("64600:" in comm for comm in pathsCommunitiesPoisonsTuple[1])]) for pathsCommunitiesPoisonsLists in pathsWithoutDirectTier1UpstreamsInThem]
	


	pathCountsOnlyVultrCommunities = [len([pathsCommunitiesPoisonsTuple for pathsCommunitiesPoisonsTuple in pathsCommunitiesPoisonsLists if all("64600:" in comm for comm in pathsCommunitiesPoisonsTuple[1])]) for pathsCommunitiesPoisonsLists in pathsList]
	pathCounts = [len(p) for p in pathsList]
	flattendPaths = [p for pl in pathsList for p in pl]
	asPaths = [p[0] for p in flattendPaths]
	communitySets = [p[1] for p in flattendPaths]
	#allUsedCommunities = set()
	#for communitySet in communitySets:
	#	for community in communitySet:
	#		allUsedCommunities.add(community)
	#print(json.dumps(list(allUsedCommunities)))
	#exit()
	asns = [asn for asPath in asPaths for asn in asPath]
	asnsAndCounts = [(asn, asns.count(asn)) for asn in set(asns)]
	asnsAndCounts.sort(key = lambda asnAndCount: -asnAndCount[1])
	print(asnsAndCounts[3:20])



	pathCountsWithoutDirectTier1Upstreams = replace0sWith1s(pathCountsWithoutDirectTier1Upstreams)
	pathCountsWithoutDirectTier1UpstreamsOnlyVultrCommunities = replace0sWith1s(pathCountsWithoutDirectTier1UpstreamsOnlyVultrCommunities)
	pathCountsOnlyVultrCommunities = replace0sWith1s(pathCountsOnlyVultrCommunities)
	pathCounts = replace0sWith1s(pathCounts)
	


	pathCountsWithoutDirectTier1Upstreams.sort()
	pathCountsWithoutDirectTier1UpstreamsOnlyVultrCommunities.sort()
	pathCountsOnlyVultrCommunities.sort()
	pathCounts.sort()
	


	pathCountAverage = sum(pathCounts) / len(pathCounts)
	print(f"Max paths: {pathCounts[-1]}, min paths: {pathCounts[0]}, median paths: {pathCounts[int(len(pathCounts) * .5)]}, average paths: {pathCountAverage}")
	
	#plt.plot(pathCountsWithoutDirectTier1Upstreams, np.arange(0, 1, 1 / len(pathCounts)), label="Paths Found Without Tier-1 Upstreams")
	#plt.plot(pathCountsWithoutDirectTier1UpstreamsOnlyVultrCommunities, np.arange(0, 1, 1 / len(pathCounts)), label="Paths Found Without Tier-1 Upstreams Without Transitive Communities")
	
	plt.plot(pathCounts, np.arange(0, 1, 1 / len(pathCounts)), label="Paths Found")
	plt.plot(pathCountsOnlyVultrCommunities, np.arange(0, 1, 1 / len(pathCountsOnlyVultrCommunities)), label="Paths Found Using Only Vultr Communities")
	plt.xlim(0, 12.5)
	plt.xlabel("Path Count")
	plt.ylabel("CDF")
	plt.legend(loc="lower right")
	plt.show()
	#plt.hist(pathCounts, cumulative=True, label='CDF',
    #     histtype='step', alpha=0.8, color='k')
	#plt.show()
	total = len(pathCounts)
	for i in range(pathCounts[-1]):
		pathCount = i + 1
		nodeCount = len([l for l in pathCounts if l == pathCount])
		print(f"node pairs with {pathCount} different paths: {nodeCount}, fraction: {nodeCount/total}")
	#print([pl for pl in pathsList if len(pl) == 12])

	# Todo
	total = pathCountsOnlyVultrCommunities
	for i in range(pathCountsOnlyVultrCommunities[-1]):
		pathCount = i + 1
		nodeCount = len([l for l in pathCounts if l == pathCount])
		print(f"node pairs with {pathCount} different paths: {nodeCount}, fraction: {nodeCount/total}")
	


if __name__ == '__main__':
    main(parse_args())