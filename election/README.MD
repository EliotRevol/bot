# Election Analytics

Json and transcripts files must be stored. Paths are harcoded on code, they must be changed according the new directory.

## Presidential Campaign

### CSA

Parole Times downloaded from CSA website are stored (or converted if necessary) on [csa](csa) folder.

### Experiments

#### Channel Personalization

* Cosine distance calculations

#### Comparison With CSA Times

* Title Search Fetch
* Title Search Walks
* Transcript Duration
* Transcript Search

#### Comparison With First Round Results

* Fetch Based
    * Title Search
    * Watch Count
* Walk Based
    * Transcript Duration
    * Watch Count

#### Fetch Based Experiments

* Temporal Evolution Graphs vs Polls
    * Title Search
    * Watch Count
* Title Search
* Sentiment Analysis
* Watch Count per Total Count
* Watch Count per Upload Date

#### Walk Based Experiments

* Drifts
    * Homepage Drifts
    * Proposal Drifts
    * Drifts on first hop
* Watch Count / Date
* Tags
* Sentiment on transcripts
* Transcripts
* Temporal
    * Transcript Duration
    * Watch Count on title search
    * Transcripts non set (duplicated) duration
    * Comparison with polls

### Polls

For the first round, polls downloaded from nsppolls are extracted and smoothed in [election/polls](election/polls).

## Legislative

* Fetch based temporal title search
* Walk based temporal
    * Tag Search
    * Transcript Search and Non Unique Transcript Search
    * Watch Count

## Meta Channel Personalization

* Cosine distance calculations

# Plots

Plots are usually stored in [election/plots](election/plots) in same naming convention with the related experiment. Some
of them might be extracted on the experiment folder.
