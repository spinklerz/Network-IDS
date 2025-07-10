# Network Anomoly Detector

This project involves building a Anomalous Detection system using an autoencoder based on my own zeek data in which I generated about 1.2m packets of data.

## Techniques Used

- Data Processing
- Exploratory Data Analysis
- Data Visualization
- Data Analysis
- Model Building

## Libraries Used

- pandas
- seaborn
- matplotlib.pyplot
- tensorflow with keras
- sklearn train_test_split
- python
- hashlib
- pickle
- sqlite3
- numpy
- gzip
- os

## 1.) Data Extraction

- The Data set was imported from zeek using conn.log data
- Initially: 1243021 x 22 columns
- After Cleaning/Processing: 1243021 x 55

## 2.) EDA

- Heatmap on numerical values
  ![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/HeatMap.png "HeatMap")

### Conclusions

- Our histograms are one contigous block, given that network data can be very dynamic and unique I would say this is expected behavior.

### 3.) Data Processing

-
