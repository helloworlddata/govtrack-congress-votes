"""
Converts votes JSON into a flat CSV
"""

from settings import get_fetched_congress_numbers, glob_vote_files, \
                      map_vote_value, extract_bill_meta, COLLATED_DIR

from csv import DictWriter
import json

DEST_PATH = COLLATED_DIR / 'votes.csv'

META_HEADERS = ['id', 'date']
BILL_HEADERS = ['bill_id', 'bill_type']
RESULT_HEADERS = ['yes', 'no', 'present', 'not_voting']
VOTE_HEADERS = ['congress', 'category', 'chamber', 'number', 'question',
                'requires', 'result', 'result_text', 'session', 'source_url',
                'subject', 'type', 'updated_at']
AMENDMENT_HEADERS = ['amendment_' + s for s in ['author', 'number', 'type']]
ALL_HEADERS = META_HEADERS + BILL_HEADERS + RESULT_HEADERS \
              + VOTE_HEADERS + AMENDMENT_HEADERS




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
    congress_numbers = get_fetched_congress_numbers()
    print("Congress numbers found:", ', '.join(congress_numbers))

    destfile = DEST_PATH.open('w')
    destcsv = DictWriter(destfile, fieldnames=ALL_HEADERS)
    destcsv.writeheader()

    for cnum in congress_numbers:
        # e.g. ./114/votes/2015/h100/data.json
        for i, fpath in enumerate(glob_vote_files(cnum)):
            vdata = json.loads(fpath.read_text())
            row = extract_votedata(vdata)
            destcsv.writerow(row)

        print("Congress {num}: {votecount} votes".format(num=cnum, votecount=i+1))

    destfile.close()
