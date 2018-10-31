# Classifying Wildfire Size

With a warming atmosphere and expanding housing settlements, wildland fires have become more dangerous than ever. Using a dataset of 1.88 million U.S. wildfires, I try to predict what size class a fire will reach based on features known at the time of discovery. This will not replace current monitoring systems, but hopefully will help act as an alarm to bring attention to potentially overlooked fires. 

# Metric 
I choose F1 score as my metric n evaluating my models because there is a need to balance the danger to lives and property from underestimating a fire and limited resources to devote to firefighting.

# TAKE 1 (8-8-2018)
Notebook Progression:
1. Load dataset into pandas and do exploratory data analysis. 
2. Experiment with cleaning data and filling in missing information.
3. Implement cleaning functions to a subset of 10000 records to generate a dataframe for modeling, such as:
    - converting date for julian to gregorian
    - filling in county names and ID's
    - create features based on location's fire history
4. Run models with oversampling to address imbalanced classes.
5. Create 5-fold cross validation functions, both with and without oversampling. Not much signal.
6. Test scraping weather data (max_temp, precipitation, wind speed) from NOAA weather API that are known to be useful for assessing fire risk.
7. Simplify the 7 default size classes in the dataset to 3 because the extra confusion do not add much value.
<!-- 8. Run models with only 3 classes.
9. Scale up weather scraping to the 10k subset and incorporated stratified k-fold in cross validation.
10. Test model on another random 10k subset from. UNREASONABLE SCORING METHOD.
11. Test model on 10k subset randomly sampled from 500000 most recent fires. UNREASONABLE TESTING. 
12. Pivot to do more feature mining on G dataset-->
13. Extend engineered features to full dataset, but no weather features due to issues with API.
RESULTS on test data (50k subset): 0.48 recall on class 3 (large) fires, but only 0.04 F1 score. 

# TAKE 2 (soon)
1. Scrape weather from Google BigQuery public datasets.
2. Look up location altitude based on lat/long. 
3. Adjust fire history function
4. More features
<!-- 5. Redo EDA -->


