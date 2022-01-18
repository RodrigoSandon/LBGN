# Laboratory of Behavioral and Genomic Neuroscience
Supervisors: Dr. Patrick Piantadosi and Dr. Andrew Holmes

# TODO Streams
1) Include activity tracking in addition to responsiveness tracking
2) BORIS Matlab to BORIS python for approach abort data
3) Similarity map (DTW/Pearson corr) --> Decoders --> Interpretation Models
4) Including DLC --> how is movement alone impacting our analyses?
5) Include Progressive Ratio Sessions into database

# BUGS

1) I thought i fixed the truncation error, but it came back again? Need to make this fix simpler
   1) Just trim to 200 and that's it

# Main Project: ISX-ABET-DLC Pipeline

ISX-ABET-DLC is a Python library for extracting, preprocessing, aligning, and analyzing calcium activity data, behavioral data, and positional data using Inscopix (ISX), Animal Behavior Environment Test (ABET), and DeepLabCut (DLC) with 1-photon imaging data in mind.

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ISX-ABET-DLC.

```bash
pip install ISX-ABET-DLC
```

### Usage

```python
import ISX-ABET-DLC
```

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### License
[MIT](https://choosealicense.com/licenses/mit/)

# Subprojects: 
Aligning Big Brains & Atlases (ABBA), 
Merging Video Files

