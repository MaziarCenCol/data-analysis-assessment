# Internal Evaluation Guide

**For Reviewer Use Only**

This guide outlines the success criteria for the "Real World Project Opportunity" screening. The goal is to identify candidates who can handle "messy" data and think like analysts.

## Key Success Criteria

### 1. Data Cleaning & Preparation
*   **Country Standardization**: Did they notice `CA`, `Canada`, `can` are the same?
*   **JSON Parsing**: Did they successfully extract fields from the `payload` column in `events.csv`?
    *   *Strong Signal*: Creating separate columns for `voltage`, `temperature`, or separating `status` lists.
*   **Deduplication**: There are intentional duplicate users. Did they find/remove them?

### 2. Analysis & Insights
*   **Device Segmentation**:
    *   **Tuya vs Ayla**: Did they figure out that `Tuya` devices use a `status` list while `Ayla` uses `metadata/datapoint` structure?
*   **Anomaly Detection**:
    *   There is one device with **voltage spikes** (up to ~240V). Did they find it?
    *   There is a "spammy" device with unusually high event volume.
*   **Clustering / Correlation**:
    *   Did they attempt to group devices (e.g., K-Means or simple quantile binning) based on event count?
    *   Did they look for relationships between `firmware_version` and error rates/anomalies?

### 3. SQL Skills
*   **JSON Handling**: Usage of `json_extract`, `->>`, or string manipulation to get data from `payload`.
*   **Aggregations**: Correct use of `GROUP BY` with dates and device types.

### 4. Hypotheses
*   *Expected Hypothesis*: "Higher voltage correlates with device failures or specific error codes."
*   *Expected Hypothesis*: "Tuya devices report more frequently than Ayla due to different telemetry standards."

## Grading Rubric

| Level | Description |
| :--- | :--- |
| **Pass** | Parses JSON (even clumsily), finds the Country issue, produces basic charts. |
| **Strong** | Standardizes all data, identifying the Schema difference between Tuya/Ayla, finds the Voltage anomaly. |
| **Reject** | Ignores the `payload` column entirely, fails to parse JSON, or treats `CA`/`Canada` as different regions. |
