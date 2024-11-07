#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json

def parse_args():
	parser = argparse.ArgumentParser()
	# This is a CAIDA AS topology.
	parser.add_argument("-n", "--nodes_json",
						default="../terraform/terraform.tfstate")
	parser.add_argument("-n", "--nodes_json_output", # This is a written output file.
						default="../config/vultr/nodes.json")
	return parser.parse_args()


def main(args):
	tfstate = json.load(open(args.tfstate_file))


	with open(args.nodes_json_output, 'w') as f:
		json.dump(nodesJsonObject, f)


if __name__ == '__main__':
    main(parse_args())