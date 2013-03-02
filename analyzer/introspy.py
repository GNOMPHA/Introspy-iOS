#!/usr/bin/env python

""" Command-line parser for an introspy generated db. """

from sys import argv, exit
from argparse import ArgumentParser
from Analysis import Analyzer, Signature
from Signatures import signature_list

__author__	= "Tom Daniels & Alban Diquet"
__license__	= "?"
__copyright__	= "Copyright 2013, iSEC Partners, Inc."

def main(argv):
	parser = ArgumentParser(description="introspy analysis tool")
	parser.add_argument("db",
			help="the introspy-generated database to analyze")
	parser.add_argument("-r", "--html",
			action="store_true",
			help="generate an HTML report (specified with -o)")
	parser.add_argument("-o", "--outfile",
			help="destination file for HTML report")
	parser.add_argument("-s", "--signature",
			help="filter by signature class [FileSystem, HTTP, \
			UserPreferences, Pasteboard, XML, Crypto, KeyChain, \
			Schemes]")
	parser.add_argument("-n", "--no-info",
			action="store_false",
			help="Don't run signatures that are purely informational")
	args = parser.parse_args()
	analyzer = Analyzer(args.db, signature_list, args.signature, args.no_info)
	findings = analyzer.check_signatures()
	if args.html:
		try:
			from submodules.jinja2.jinja2 import Environment, PackageLoader
		except ImportError:
			print "Jinja2 (https://github.com/mitsuhiko/jinja2)" \
				"is required for HTML report generation."
			exit(1)
		env = Environment(loader=PackageLoader('introspy', 'html'))
		template = env.get_template('templates/introspy.html')
		outfile = open(args.outfile, 'w')
		outfile.write(template.render(findings=findings))
	else:
		for key in findings:
			print "# %s" % findings[key][0].sig_match
			for trace in findings[key]:
				print "  %s" % trace

if __name__ == "__main__":
	main(argv[1:])
