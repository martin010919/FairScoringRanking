import math
from typing import Dict, Tuple, List

def calculate_fair_score(total_ratings: int, score_given: int, mean_score: float) -> Tuple[float, float, Dict]:
    """
    Calculate a fair score and fair weighted score using actual completion data.
    
    Parameters:
    total_ratings (int): Total number of users (including those who gave a score from 0 to 10)
    score_given (int): Number of users who actually rated the show (1-10)
    mean_score (float): Current mean score of the anime
    
    Returns:
    Tuple[float, float, Dict]: Fair score, fair weighted score, and detailed metrics
    """
    # Constants
    MINIMUM_RATINGS = 100
    BAYESIAN_PRIOR = 7.0
    PRIOR_WEIGHT = 500
    
    # Calculate "Plan to Watch" (PTW) count
    plan_to_watch = total_ratings - score_given
    
    # Calculate completion rate (excluding PTW)
    completion_rate = score_given / total_ratings if total_ratings > 0 else 0
    
    # Base confidence from number of completed ratings
    rating_confidence = min(1.0, score_given / MINIMUM_RATINGS)
    
    # Adjust confidence based on completion rate
    completion_factor = completion_rate * 0.5 + 0.5  # Ranges from 0.5 to 1.0
    adjusted_confidence = rating_confidence * completion_factor
    
    # Calculate engagement score (how many people actually rate after adding)
    engagement_bonus = math.log10(score_given + 1) * completion_rate * 0.1
    
    # Popularity bonus considering both ratings and total interest
    popularity_bonus = (
        math.log10(score_given + 1) * 0.06 +
        math.log10(total_ratings + 1) * 0.02
    )
    
    # Bayesian average calculation
    bayesian_score = (
        (PRIOR_WEIGHT * BAYESIAN_PRIOR + score_given * mean_score) /
        (PRIOR_WEIGHT + score_given)
    )
    
    # Final score calculation
    fair_score = (bayesian_score * adjusted_confidence) + engagement_bonus + popularity_bonus
    
    # Fair weighted score calculation (giving more weight to shows with more ratings)
    fair_weighted_score = fair_score * (score_given / total_ratings) if total_ratings > 0 else fair_score
    
    # Compile metrics for analysis
    metrics = {
        "plan_to_watch": plan_to_watch,
        "completion_rate": completion_rate * 100,
        "confidence": adjusted_confidence * 100,
        "engagement_bonus": engagement_bonus,
        "popularity_bonus": popularity_bonus
    }
    
    return max(1.0, min(10.0, fair_score)), max(1.0, min(10.0, fair_weighted_score)), metrics

# Updated dataset with the given data
dataset = [
    ("Monogatari S1", 61094, 8.91, 31246, 29847),
    ("Monogatari S2", 24045, 8.90, 11574, 12471),
    ("Monogatari S3", 19626, 8.83, 8321, 11306),
    ("Mushoku Tensei", 91393, 8.83, 65658, 25732),
    ("Spice and Wolf", 66209, 8.82, 32226, 33981),
    ("86", 43586, 8.82, 21175, 22409),
    ("COTE p1", 89803, 8.81, 56219, 33579),
    ("Re:Zero", 73645, 8.80, 40938, 32707),
    ("Honzuki no Gekokujou", 16766, 8.78, 9523, 7241),
    ("COTE p2", 38809, 8.78, 24946, 13858)
]

# Adding fair score, fair weighted score, and score distribution to the dataset
updated_dataset: List[Tuple[str, int, float, int, int, float, float]] = []
for anime, total_ratings, mean_score, score_given, plan_to_watch in dataset:
    fair_score, fair_weighted_score, _ = calculate_fair_score(total_ratings, score_given, mean_score)
    updated_dataset.append((anime, total_ratings, mean_score, score_given, plan_to_watch, fair_score, fair_weighted_score))

# Sort the dataset by the fair score in descending order
sorted_dataset = sorted(updated_dataset, key=lambda x: x[5], reverse=True)

# Prepare data for table output
header = ["Title", "Total Ratings", "Mean Score", "Score Given", "Plan to Watch", "Fair Score", "Fair Weighted Score"]
print(f"{' | '.join(header)}")
print("-" * 90)  # Separator line

for entry in sorted_dataset:
    print(f"{entry[0]:<20} | {entry[1]:<15} | {entry[2]:<10} | {entry[3]:<10} | {entry[4]:<15} | {entry[5]:<12} | {entry[6]:<17}")
