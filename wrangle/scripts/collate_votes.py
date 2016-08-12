"""
Converts votes JSON into a flat CSV
"""
from csv import DictWriter
from pathlib import Path
import json
META_HEADERS = ['id', 'date']
BILL_HEADERS = ['bill_' + h for h in ['congress', 'number', 'type']]
RESULT_HEADERS = ['yes', 'no', 'present', 'not_voting']
VOTE_HEADERS = ['congress', 'category', 'chamber', 'number', 'question',
                'requires', 'result', 'result_text', 'session', 'source_url',
                'subject', 'type', 'updated_at']
ALL_HEADERS = META_HEADERS + RESULT_HEADERS + BILL_HEADERS + VOTE_HEADERS

FETCHED_DIR = Path('wrangle', 'corral', 'fetched', 'congress')
# SRC_DIR = FETCHED_DIR.joinpath('114', 'bills', 'hr')
DEST_PATH = Path('wrangle', 'corral', 'compiled', 'votes.csv')
DEST_PATH.parent.mkdir(exist_ok=True, parents=True)

"""
todos:
determine if bill_congress is always the same as congress
if result == result_text
"""



def extract_votedata(vote):
    row = {'id': vote['vote_id'], 'date': vote['date']}
    for h in BILL_HEADERS:
        row[h] = vote[h.split('_')[-1]]
    for h in VOTE_HEADERS:
        row[h] = vote.get(h)
    # https://www.govtrack.us/blog/2009/11/18/aye-versus-yea-whats-the-difference/
    # set yes,no,present,not_voting to 0 at the start
    for h in RESULT_HEADERS:
        row[h] = 0
    for pos, entries in vote['votes'].items():
        if pos in ['Aye', 'Yea']:
            position = 'yes'
        elif pos in ['No', 'Nay']:
            position = 'no'
        elif pos is 'Not Voting':
            position = 'not_voting'
        elif pos is 'Present':
            position = 'present'
        else:
            position = None
        if position:
            row[position] += len(entries)
    return row



if __name__ == '__main__':
    destfile = DEST_PATH.open('w')
    destcsv = DictWriter(destfile, fieldnames=ALL_HEADERS)
    destcsv.writeheader()

    for congressnum in range(110, 114+1):
        globpattern = str(Path(str(congressnum), 'votes', '*', '*', 'data.json'))
        for i, fpath in enumerate(FETCHED_DIR.glob(globpattern)):
            vdata = json.loads(fpath.read_text())
            row = extract_votedata(vdata)
            destcsv.writerow(row)

        print("Congress {num}: {votecount} votes".format(num=congressnum, votecount=i+1))



    destfile.close()
