"""
Converts votes JSON into a flat CSV
"""

from settings import map_vote_value, extract_bill_meta


import argparse
from csv import DictWriter
import json
from loggy import loggy
from pathlib import Path
from sys import stdout


META_HEADERS = ['id', 'date']
BILL_HEADERS = ['bill_id', 'bill_type']
RESULT_HEADERS = ['yes', 'no', 'present', 'not_voting']
VOTE_HEADERS = ['congress', 'category', 'chamber', 'number', 'question',
                'requires', 'result', 'result_text', 'session', 'source_url',
                'subject', 'type', 'updated_at']
AMENDMENT_HEADERS = ['amendment_' + s for s in ['author', 'number', 'type']]
ALL_HEADERS = META_HEADERS + BILL_HEADERS + RESULT_HEADERS \
              + VOTE_HEADERS + AMENDMENT_HEADERS


LOGGY = loggy('collate_votes')


def extract_votedata(vote):
    row = {'id': vote['vote_id'], 'date': vote['date']}
    # bill_id is constructed as a convenience when joining to the bills database
    _bm = extract_bill_meta(vote)
    if _bm:
        row['bill_id'] = _bm['id']
        row['bill_type'] = _bm['type']
    else:
        row['bill_id'] = row['bill_type'] = None

    for h in VOTE_HEADERS:
        row[h] = vote.get(h)

    # not all votes are amendments
    amendment = vote.get('amendment')
    if amendment:
        for h in AMENDMENT_HEADERS:
            i = h.split('_')[-1]
            row[h] = amendment.get(i)
    else:
        row.update({h: None for h in AMENDMENT_HEADERS})

    # https://www.govtrack.us/blog/2009/11/18/aye-versus-yea-whats-the-difference/
    # set yes,no,present,not_voting to 0 at the start
    for h in RESULT_HEADERS:
        row[h] = 0
    for vval, members in vote['votes'].items():
        voteval = map_vote_value(vval)
        if voteval:
            row[voteval] += len(members)
    return row


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Creates a simplified CSV of votes for the JSON in a given directory")
    parser.add_argument('srcdir', type=str, help="directory of JSON to recursively parse for")
    args = parser.parse_args()
    srcdir = args.srcdir
    # srcir is something like congress/100/votes
    files = list(Path(srcdir).rglob('data.json')) # , '*', '*', 'data.json')
    LOGGY.info('%s files in %s' % (len(files), srcdir))
    votes = []

    for fn in files:
        d = json.loads(fn.read_text())
        votes.append(extract_votedata(d))


    csvout = DictWriter(stdout, fieldnames=ALL_HEADERS)
    csvout.writeheader()
    for vote in sorted(votes, key=lambda x: int(x['number'])):
        csvout.writerow(vote)

