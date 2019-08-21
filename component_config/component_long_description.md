# 2Performant Affiliate Extractor

The 2Performant extractor allows to download all commissions and their transactions.

To successfully use the extractor, a username and password used to access [network.2performant.com](https://network.2performant.com/) is needed.

## Configuration

A configuration of 3 mandatory parameters is required. A sample configuration of the component can be found in [component's repository](https://bitbucket.org/kds_consulting_team/kds-team.ex-2performant/src/master/component_config/sample-config/).

- username (`username`) - a username used to login to 2performant;
- password (`#password`) - a password associated with username;
- month delta (`monthsBack`) - a positive integer marking the amount of months for which to download commissions.
- incremental load (`incremental`) - a boolean marking, whether incremental load should be used

## Output

A table with commissions returned by the API. Table is loaded incrementally with column `id` used as primary key.