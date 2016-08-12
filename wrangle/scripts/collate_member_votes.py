
from settings import get_fetched_congress_numbers, glob_vote_files, \
                      map_vote_value, extract_bill_meta, map_party_value, COLLATED_DIR

from csv import DictWriter
import json

DEST_PATH = COLLATED_DIR / 'member_votes.csv'

BILL_HEADERS = ['bill_id']
MEMBER_HEADERS = ['member_id', 'member_party', 'member_state']
VOTE_HEADERS = ['vote_id', 'congress', 'chamber']
RESULT_HEADERS = ['vote', 'vote_value']
ALL_HEADERS = VOTE_HEADERS + BILL_HEADERS + MEMBER_HEADERS + RESULT_HEADERS


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
    congress_numbers = get_fetched_congress_numbers()
    print("Congress numbers found:", ', '.join(congress_numbers))

    destfile = DEST_PATH.open('w')
    destcsv = DictWriter(destfile, fieldnames=ALL_HEADERS)
    destcsv.writeheader()

    for cnum in congress_numbers[5:]:
        # e.g. ./114/votes/2015/h100/data.json
        xct = 0
        for fpath in glob_vote_files(cnum):
            vdata = json.loads(fpath.read_text())
            votemeta = extract_vote_meta(vdata)
            for member in extract_members_votes(vdata):
                member.update(votemeta)
                destcsv.writerow(member)
                xct += 1

        print("Congress {num}: {votecount} member votes".format(num=cnum, votecount=xct))

    destfile.close()
