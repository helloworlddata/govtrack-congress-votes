Source: https://github.com/unitedstates/congress/wiki/votes

# Votes

This project collects data on roll call votes, which are the sorts of votes in which the individual positions of legislators is recorded. Other sorts of votes such as unanimous consent requests and voice votes are not collected here.

Congress publishes roll call vote data in XML starting in 1990 (101st Congress, 2nd session) for the House and 1989 (101st Congress, 1st Session) for the Senate. Senate votes are numbered uniquely by session. Sessions roughly follow calendar years, and there are two sessions per Congress. House vote numbering continues consecutively throughout the Congress.

## Scraping votes

    ./run votes [--force [--fast] ]

The script will cache all downloaded pages, and it will not re-fetch them from the network unless a `--force` flag is passed. The `--fast` flag will have the scraper download only votes taken in the last three days, which is the time during which most vote changes and corrections are posted.

You can supply a few kinds of flags, such as limit and congress as above. Votes are grouped by the Senate and House into two sessions per Congress, which (in modern times) roughly follow the calendar years. To get votes from 2012, run:

    ./run votes --congress=112 --session=2012

To get only a specific vote, pass in the ID for the vote. For the Senate vote 50 in the 2nd session of the 112th Congress:

    ./run votes --vote_id=s50-112.2012


## Output Data Format

Every vote has a JSON file, `data.json`, with fields related to a votes's ID, result, and individual Member votes. There is also a corresponding XML file, `data.xml`, which is roughly compatible with GovTrack's legacy data format; however, the XML format is not documented, and is not particularly recommended.

The output files are in the following location:

    data/[congress]/votes/[session]/[chamber][number]/data.{json.xml}

See the (bills documentation)[Bills] for the definition of `congress`.

The examples below use data excerpts where possible from [House Vote #202, 113th Congress, 1st Session](https://www.govtrack.us/congress/votes/113-2013/h202).

### Basic information

```json
{
  "chamber": "h", 
  "congress": 113, 
  "date": "2013-06-05T22:42:00-04:00", 
  "number": 202, 
  "session": "2013", 
  "source_url": "http://clerk.house.gov/evs/2013/roll202.xml", 
  "updated_at": "2013-07-18T22:40:39-04:00", 
  "vote_id": "h202-113.2013",
}
```

The basic information indicates the Congress, session, chamber, and number of the roll call vote, which uniquely identify it. The `vote_id` combines this data into a single string. The session is a string and is the name of a calendar year, but beware that the actual dates of congressional sessions do not follow calendar years. They are bounded by the start and end of the Congress and by the winter recess dates.

The `date` gives the date or date and time at which the vote occurred.

`source_url` is the URL from which the data was scraped and is also human-readable and suitable for linking an end user to a primary source.

`updated_at` is the date and time that the JSON file was last saved. It reflects the time the scraper was run and is not metadata about the vote itself.

### What the vote was about

```json
{
  "category": "amendment", 
  "question": "On Agreeing to the Amendment: Amendment 24 to H R 2217", 
  "type": "On the Amendment"
}
```

These fields describe what the vote was about.

`type` is a semi-normalized string indicating the kind of the vote, while `question` is the full description of the subject of the vote as provided by the House or Senate.

`category` further normalizes the vote type into one of: passage, passage-suspension, amendment, cloture, nomination, treaty, recommit, quorum, leadership, conviction, veto-override, procedural, or unknown. Consult the source code for the meanings of these codes.

### The result

```json
{
  "requires": "1/2", 
  "result": "Failed", 
  "result_text": "Failed"
}
```

The `requires` field indicates what was required for the vote to succeed. This is a string as provided by the House or Senate.

`result` and `result_text` are free-form strings indicating the result of the vote, as given by the House and Senate.

### Related documents

```json
{
  "amendment": {
    "author": "Ryan of Ohio Amendment", 
    "number": 24, 
    "type": "h-bill"
  }, 
  "bill": {
    "congress": 113, 
    "number": 2217, 
    "type": "hr"
  }
}
```

If the vote is related to a bill, amendment, nomination, or treaty, the related document is listed.

Note that a vote may be related to a bill but *not* be the vote on its passage, such as if it is a vote on an amendment or a motion related to the bill.
