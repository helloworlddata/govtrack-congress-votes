from pathlib import Path

FETCHED_DIR = Path('wrangle', 'corral', 'fetched', 'congress')
FETCHED_DIR.mkdir(exist_ok=True, parents=True)
COLLATED_DIR = Path('wrangle', 'corral', 'collated')
COLLATED_DIR.mkdir(exist_ok=True, parents=True)

VOTE_VALUE_MAP = {
    'Aye': 'yes',
    'Yea': 'yes',
    'No': 'no',
    'Nay': 'no',
    'Present': 'present',
    'Not Voting': 'not_voting',
}

PARTY_VALUE_MAP = {
    'Republican': 'R',
    'Democrat': 'D',
    'Independent': 'I',
    'ID': 'ID'
}

def map_party_value(party_val):
    if len(party_val) == 1:
        return party_val
    else:
        # we want this to purposely break
        # if there is a value other than Repub/Demo/Independent
        return PARTY_VALUE_MAP[party_val]

def extract_bill_meta(votedata):
    bill = votedata.get('bill')
    if bill:
        meta = {h: bill[h] for h in ['type', 'number', 'congress']}
        # e.g. hr3590-111
        meta['id'] = bill['type'] + str(bill['number']) + '-' + str(bill['congress'])
        return meta
    else:
        return None


def get_fetched_congress_numbers():
    return sorted([p.name for p in FETCHED_DIR.glob('*')])


def glob_vote_files(congress_number):
    globpattern = str(Path(congress_number, 'votes', '*', '*', 'data.json'))
    return FETCHED_DIR.glob(globpattern)


def map_vote_value(vote_val):
    return VOTE_VALUE_MAP.get(vote_val)

