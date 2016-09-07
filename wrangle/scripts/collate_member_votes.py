from settings import map_party_value, map_vote_value, extract_bill_meta

import argparse
from csv import DictWriter
import json
from loggy import loggy
from pathlib import Path
from sys import stdout


BILL_HEADERS = ['bill_id']
MEMBER_HEADERS = ['member_id', 'member_party', 'member_state']
VOTE_HEADERS = ['vote_id', 'congress', 'chamber']
RESULT_HEADERS = ['vote', 'vote_value']
ALL_HEADERS = VOTE_HEADERS + BILL_HEADERS + MEMBER_HEADERS + RESULT_HEADERS


LOGGY = loggy('collate_votes')


def extract_vote_meta(votedata):
    meta = {'vote_id': votedata['vote_id'], 'congress': votedata['congress'], 'chamber': votedata['chamber']}
    bm = extract_bill_meta(votedata)
    if bm:
        meta['bill_id'] = bm['id']
    else:
        meta['bill_id'] = None
    return meta

def extract_members_votes(votedata):
    votes = votedata['votes'].items()
    for votetext, members in votes:
        voteval = map_vote_value(votetext)
        for m in members:
            if m == 'VP': # for when the VP casts a tie breaking vote
                row = {
                    'member_id': 'VP',
                    'member_party': None,
                    'member_state': None,
                    'vote': votetext,
                    'vote_value': voteval
                }
            else:
                row = {
                    'member_id': m['id'],
                    'member_party': map_party_value(m['party']),
                    'member_state': m['state'],
                    'vote': votetext,
                    'vote_value': voteval
                }
            yield row




if __name__ == '__main__':
    parser = argparse.ArgumentParser("Creates a simplified CSV of votes by member for the JSON in a given directory")
    parser.add_argument('srcdir', type=str, help="directory of JSON to recursively parse for")
    args = parser.parse_args()
    srcdir = args.srcdir
    # srcir is something like congress/100/votes
    files = list(Path(srcdir).rglob('data.json')) # , '*', '*', 'data.json')
    LOGGY.info('%s files in %s' % (len(files), srcdir))
    membervotes = []

    for fn in files:
        d = json.loads(fn.read_text())
        votemeta = extract_vote_meta(d)
        for member in extract_members_votes(d):
            member.update(votemeta)
            membervotes.append(member)

    csvout = DictWriter(stdout, fieldnames=ALL_HEADERS)
    csvout.writeheader()
    for vote in sorted(membervotes, key=lambda x: (x['vote_id'], x['member_id'])):
        csvout.writerow(vote)


