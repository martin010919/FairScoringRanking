# Anime Fair Score Calculation

## Overview
This project is designed to calculate and analyze anime ratings using a **fair score** system. The goal is to provide an enhanced evaluation of anime shows by factoring in the number of users who have rated the anime, the completion rate of ratings, and various engagement and popularity factors.

## Features
- **Fair Score**: A score that is calculated using a Bayesian average and adjusted based on the confidence derived from the number of users who rated the show and the completion rate of ratings.
- **Fair Weighted Score**: A variant of the fair score that gives more weight to anime shows with a higher percentage of ratings compared to their total viewership.
- **Score Distribution**: The distribution of ratings given to the anime (including how many gave scores from 1 to 10 and how many gave a score of 0 for "Plan to Watch").
- **Ranking**: The list of anime shows can be ranked based on the fair score in descending order, making it easier to compare shows according to the adjusted rating values.

## Calculation Rules

### 1. **Fair Score Calculation**
   The fair score is calculated using the following factors:
   - **Bayesian Average**: Combines the mean score of the anime with a weighted prior score. The prior score is based on a predefined value, and it adjusts the score for less popular shows with fewer ratings.
   - **Rating Confidence**: The confidence in the ratings is adjusted based on the number of ratings received, with more confidence placed on shows with a larger number of ratings (with a minimum of 100 ratings).
   - **Completion Rate**: The completion rate is the ratio of users who rated the show (with scores from 1-10) to the total number of users who interacted with the show, including those who marked it as "Plan to Watch" (score 0). Higher completion rates increase the confidence in the fair score.
   - **Engagement Bonus**: This bonus is applied based on the number of ratings given and the completion rate. The more users engage with the rating system, the higher the engagement bonus.
   - **Popularity Bonus**: A weighted bonus that accounts for both the total number of ratings and the number of completed ratings. Shows with more user interest and more ratings will receive a higher bonus.

### 2. **Fair Weighted Score Calculation**
   The fair weighted score is calculated similarly to the fair score, but with an additional adjustment for the percentage of users who rated the show (1-10) versus those who didn't rate (Plan to Watch). Shows with a higher percentage of ratings are given more weight in this calculation.

### 3. **Score Distribution**
   The score distribution includes:
   - **Total Ratings**: The total number of users who interacted with the show, including those who rated (1-10) and those who marked it as "Plan to Watch" (score 0).
   - **Score Given (1-10)**: The number of users who rated the show with scores ranging from 1 to 10.
   - **Plan to Watch (Score 0)**: The number of users who marked the show as "Plan to Watch" (score 0).

### 4. **Ranking**
   The anime shows are ranked based on the **fair score** in descending order, allowing users to easily compare the relative quality of different anime shows as adjusted by the fair score calculation.

## Data Format
The dataset contains the following columns:
- **Title**: The name of the anime.
- **Total Ratings**: The total number of users who interacted with the show (including both those who rated and those who marked as "Plan to Watch").
- **Mean Score**: The current average score of the anime (based on ratings 1-10).
- **Score Given (1-10)**: The number of users who rated the show with scores from 1 to 10.
- **Plan to Watch (Score 0)**: The number of users who marked the show as "Plan to Watch" (score 0).
- **Fair Score**: The calculated fair score based on the methodology described above.
- **Fair Weighted Score**: The fair score adjusted for the percentage of ratings to total interactions.
  
## Example Output
The output is presented as a table where each row contains the following columns:
- **Title**: The name of the anime.
- **Total Ratings**: The total number of users who interacted with the show.
- **Mean Score**: The average score of the show.
- **Score Given (1-10)**: The number of ratings given (scores 1-10).
- **Plan to Watch (Score 0)**: The number of users who marked the show as "Plan to Watch."
- **Fair Score**: The calculated fair score for the anime.
- **Fair Weighted Score**: The calculated fair weighted score for the anime.

The table is sorted by the fair score in descending order.

## Usage
To use the program, simply input the dataset into the script, and it will automatically compute the fair score, fair weighted score, and score distribution for each anime. The resulting output will be displayed as a neatly formatted table with the anime titles ranked by their fair scores.
"""

# Saving the content into a README.md file
readme_path = '/mnt/data/README.md'
with open(readme_path, 'w') as file:
    file.write(readme_content)

readme_path  # Returning the path for download

