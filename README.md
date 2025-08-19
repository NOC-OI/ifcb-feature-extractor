> [!WARNING]
> This repo has been deprecated, functionality has been merged into [ifcbproc](https://github.com/NOC-OI/ifcbproc)

# ifcb-feature-extractor
A simple CLI tool for easy use of the [WHOI ifcb-features](https://github.com/WHOIGit/ifcb-features) library. Only a few modifications have been made to make it easier to install.
## Install
Install all dependencies in requirements.txt and then you're good to go!
## Usage
```python3 cli.py ./testdata/D20191211T034109_IFCB010.hdr -o ./testout.csv```
This will produce v4 feature files in the same format as the earlier v2 classifier outputs found in Heidi Sosik's [ifcb-analysis](https://github.com/hsosik/ifcb-analysis) MATLAB library. These results will not be identical, so you must ensure any comparitive studies are done against v4 feature compatible classifiers.

