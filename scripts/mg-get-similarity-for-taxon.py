#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from mglib import AUTH_LIST, VERSION, API_URL, get_auth_token, urlencode, stdout_from_url

prehelp = """
NAME
    mg-get-similarity-for-taxon

VERSION
    %s

SYNOPSIS
    mg-get-similarity-for-taxon [ --help, --user <user>, --passwd <password>, --token <oAuth token>, --id <metagenome id>, --name <taxon name>, --level <taxon level>, --source <datasource>, --evalue <evalue negative exponent>, --identity <percent identity>, --length <alignment length> ]

DESCRIPTION
    Retrieve taxa annotated sequences for a metagenome filtered by taxon containing inputted name.
"""

posthelp = """
Output
    BLAST m8 format - tab-delimited list of: query sequence id, hit m5nr id, percentage identity, alignment length, number of mismatches, number of gap openings, query start, query end, hit start, hit end, e-value, bit score, semicolon seperated list of annotations

EXAMPLES
    mg-get-similarity-for-taxon --id "mgm4441680.3" --name Lachnospiraceae --level family --source RefSeq --evalue 8

SEE ALSO
    -

AUTHORS
    %s
"""

def main(args):
    ArgumentParser.format_description = lambda self, formatter: self.description
    ArgumentParser.format_epilog = lambda self, formatter: self.epilog
    parser = ArgumentParser(usage='', description=prehelp%VERSION, epilog=posthelp%AUTH_LIST)
    parser.add_argument("--id", dest="id", default=None, help="KBase Metagenome ID")
    parser.add_argument("--url", dest="url", default=API_URL, help="communities API url")
    parser.add_argument("--user", dest="user", default=None, help="OAuth username")
    parser.add_argument("--passwd", dest="passwd", default=None, help="OAuth password")
    parser.add_argument("--token", dest="token", default=None, help="OAuth token")
    parser.add_argument("--name", dest="name", default=None, help="taxon name to filter by")
    parser.add_argument("--level", dest="level", default=None, help="taxon level to filter by")
    parser.add_argument("--source", dest="source", default='SEED', help="datasource to filter results by, default is SEED")
    parser.add_argument("--evalue", dest="evalue", default=5, help="negative exponent value for maximum e-value cutoff, default is 5")
    parser.add_argument("--identity", dest="identity", default=60, help="percent value for minimum % identity cutoff, default is 60")
    parser.add_argument("--length", dest="length", default=15, help="value for minimum alignment length cutoff, default is 15")
    
    # get inputs
    opts = parser.parse_args()
    if not opts.id:
        sys.stderr.write("ERROR: id required\n")
        return 1
    
    # get auth
    token = get_auth_token(opts)
    
    # build url
    params = [ ('source', opts.source),
               ('evalue', opts.evalue),
               ('identity', opts.identity),
               ('length', opts.length),
               ('type', 'organism') ]
    if opts.name:
        params.append(('filter', opts.name))
        if opts.level:
            params.append(('filter_level', opts.level))
    url = opts.url+'/annotation/similarity/'+opts.id+'?'+urlencode(params, True)
    
    # output data
    stdout_from_url(url, auth=token)
    
    return 0
    

if __name__ == "__main__":
    sys.exit(main(sys.argv))
