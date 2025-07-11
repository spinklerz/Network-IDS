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
- After Cleaning/Processing: 1243021 x 55 columns

## 2.) EDA

Heatmap on numerical values
  
  ![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/HeatMap.png "HeatMap")
Notes: 
  - Notice features like dst_bytes and the relationship it has with orig_pkts and resp_pkts.
  - Whats interesting to notice is that this relationship tells us that when a server sends a larger payload the amount of packets sent by the client is also increased (dst_bytes/orig_pkts). This suggests the client is sending more ACK's to the server for the larger payloads it recieves. Which makes sense in a general sense.
  - orig_ip_bytes and resp_ip_bytes while interesting I don't think contribute much to data and will only server as noise for traning which is why I decided to remove them in the processing phase.
***

Heatmap without orig_ip_bytes and resp_ip_bytes

![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/HeatMap2.png "HeatMap")

Notes: 
- This visualization makes things a lot clearer and gives us a sense of direction when feature engineering

***

Feature distribution

![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/Hist.png "Histogram")

Notes: 
- A lot of unqiue values which makes sense for network data
- Source port distribution highlights the use of ephemeral ports
  
***

Network Traffic 

![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/Network_Traffic_2025-02-22.png "Network Traffic")

Notes: 
- Cool to see network traffic visualization, per each day, the example above is on 2025-02-22 data
- You can find the rest of the distributions and more visualization in the file ./Notebooks/03_preprocessing_cleaning_feature_engineering.ipynb

### Conclusions

- Our histograms are one contigous block, given that network data can be very dynamic and unique I would say this is expected behavior.

### 3.) Data Processing

-
