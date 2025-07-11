# Network Anomaly Detector

This project involves building an anomalous detection system using an autoencoder based on my own Zeek data, in which I generated about 1.2 million packets of data.

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

- TensorFlow with Keras

- sklearn train_test_split

- Python

- hashlib

- pickle

- sqlite3

- numpy

- gzip

- OS

## 1.) Data Extraction

- The data set was imported from Zeek using conn.log data.

- Initially: 1243021 x 22 columns

- After Cleaning/Processing: 1243021 x 55 columns

## 2.) EDA

Heatmap on numerical values



![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/HeatMap.png "HeatMap")

Notes:

- Notice features like dst_bytes and the relationship it has with orig_pkts and resp_pkts.

- What's interesting to notice is that this relationship tells us that when a server sends a larger payload, the amount of packets sent by the client is also increased (dst_bytes/orig_pkts). This suggests the client is sending more ACKs to the server for the larger payloads it receives. Which makes sense in a general sense.

- orig_ip_bytes and resp_ip_bytes, while interesting I don't think they contribute much to data and will only serve as noise for training, which is why I decided to remove them in the processing phase.

***

Heatmap without orig_ip_bytes and resp_ip_bytes

![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/HeatMap2.png "HeatMap")

Notes:

- This visualization makes things a lot clearer and gives us a sense of direction when feature engineering.

***

Feature distribution

![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/Hist.png "Histogram")

Notes:

- A lot of unique values, which makes sense for network data

- Source port distribution highlights the use of ephemeral ports.



***

Network Traffic

![alt text:](https://github.com/spinklerz/Network-IDS/blob/main/images/Network_Traffic_2025-02-22.png "Network Traffic")

Notes:

- Cool to see network traffic visualization; per each day, the example above is on 2025-02-22 data.

- You can find the rest of the distributions and more visualizations in the file. /Notebooks/02_Exploratory_Data_Analysis.ipynb

***

Top Protocols

![alt text:](https://github.com/spinklerz/Network-IDS/blob/main/images/TopProtocols.png "Top Protocols")

***

Top Services

![alt text:](https://github.com/spinklerz/Network-IDS/blob/main/images/TopServices.png "Top Services")

Notes:

- "-" means Zeek could not determine the service.

- It's interesting to see how populated DNS queries are, as on Wireshark I usually don't see too many.

### 3.) Data Processing

- data type assignment

- Feature-engineered values: dst_bytes_per_orig_pkt, dst_bytes_per_resp_pkt

- Replaced infinite values from the feature-engineered values.

- Dropped rows 'orig_pkts', 'dst_bytes', 'resp_pkts', 'orig_ip_bytes', 'resp_ip_bytes', 'missed_bytes', 'tunnel_parents', 'ts'

- Directly translated IPv4 and IPv6 addresses into integers. These integers were too large, so we decided to use modulo to limit the size of the address by capping it at 65535 for an IPv4 and 4294967295 for an IPv6 address.

- decided to one-hot encode features 'proto', 'service', 'conn_state', 'local_orig', and 'local_resp'

- decided to hash 'uid' and 'history' due to the fact they were too unique and would cause the data set to inflate to around 9000 features

### 4.) Model

- Scaled data with StandardScaler

- Train/test/validation data set splits are 20%/67.5%/12.5%.

- Autoencoder architecture 55 -> 32 -> 16 -> 32 -> 55

- ReLU activation function

- Used MSE to calculate loss

- Implemented early callback if no improvement after 3 epochs



***

Visualization of the Train/Validation Loss

![alt text](https://github.com/spinklerz/Network-IDS/blob/main/images/TVloss.png "T/V loss")

***

Training Reconstruction Loss Graph

![alt text:](https://github.com/spinklerz/Network-IDS/blob/main/images/TrainReconstruction.png "Reconstruction")

***

### 5.) Results

- Training loss: 0.2131

- Validation loss: 0.2857

- Test loss: 0.3853

- These results likely indicate overfitting given the huge increase between training loss and test loss.

### 6.) Deployment

- Batch processing

- Wait until Zeek transforms the current conn.log data into a *.gz file.

- Grab the *.gz file, then preprocess and scale it.

- Flag only 5% of traffic as anomalous.

- Append these 5% to an SQLite3 server.

- Then dump the SQLite3 DB to see results.

### 7.) Future Plans

- More comprehensive visualization; plan to create a dashboard for Zeek data logs.

- More deployment and performance testing

- More aggressive model

- Implement temporal features.

- Higher quality data: The truth is conn.log does give me a lot of useful information, but it lacks in tracking things like volumetric floods and attacks that could happen on workstations. I only use this machine for work-related stuff and generating realistic or high-quality data for HTTP servers, FTP servers, SMB servers, etc. Data from my own machine is difficult to say the least.

