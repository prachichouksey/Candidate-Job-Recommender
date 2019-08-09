# Candidate Job Recommendation

## Overview
The goal of project is to recommend relevant candidates based on their resume for a job. 
Job search has become one of the most challenging tasks in the IT industry. Recruitment teams in IT companies spend major amount of time screening resumes amongst which most of the candidates are rejected. The job recommender system will fetch the user skills (resume skills) and suggest most relevant jobs from online job portal (Indeed/ Glassdoor/ LinkedIn etc.)

## Dataset
The job descriptions have been scraped from www.indeed.com 
The data has been scraped by providing various keywords for technologies and title. However, there is some redundant data, rows with missing values etc.
This data has been preprocessed to remove redundancies and missing values to get more reliable output.
Unnecessary stopwords and characters have also been removed to get better recommendations.
The job description is also converted to comma separated keywords in order to perform content based recommendation against user resume.

## Calculating Similarity
For calculating similarity between job description and candidate resume, content based recommendation system has been implemented as this is the best option when both the values are in the form of content instead of ratings or any other numeric data.
TF-IDF vectors have been created for the job description and similarity is calculated with the resume vectors.
Apart from the content match, there are other factors as well which play a significant role in resume scoring for a candidate like experience, role, skill etc and a final rating is calculated based on the weightage for each factor.
We are giving weightage to each resume in 4 ways as mentioned below:
1. 40% weightage to Experience matching of Resume to job description
2. 40% Weightage of Skill in Resume to job description matching
3. 15% weightage of job description to Resume matching using Cosine Distance
4. 5% weightage of Non-Technical skill matching of Resume to job description

All above weightage can be easily changed in coding configuration.

## Repository structure
```

├── data-scrape_indeed
|   └── contains the code to scrape indeed.com and refine the dataset
|
├── web_app
|   ├── Flask web application to give basic UI to upload job description, resume and view similarity

```
In order to start the application, navigate to web_app folder and execute app.py as python app.py on terminal
Open localhost:3000 and calculate score for candidates.
