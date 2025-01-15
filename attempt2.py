import math
from typing import Dict, Tuple

def calculate_fair_score(total_ratings: int, score_given: int, mean_score: float, popularity_rank: int) -> Tuple[float, Dict]:
    """
    Calculate a fair score using actual completion data.
    
    Parameters:
    total_ratings (int): Total number of users (including PTW and scored)
    score_given (int): Number of users who actually rated the show (1-10)
    mean_score (float): Current mean score of the anime
    popularity_rank (int): Rank in terms of total ratings
    
    Returns:
    Tuple[float, Dict]: Fair score and detailed metrics
    """
    # Constants
    MINIMUM_RATINGS = 100
    BAYESIAN_PRIOR = 7.0
    PRIOR_WEIGHT = 500
    
    # Calculate PTW count and metrics
    ptw_count = total_ratings - score_given
    completion_rate = score_given / total_ratings if total_ratings > 0 else 0
    
    # Base confidence from number of completed ratings
    rating_confidence = min(1.0, score_given / MINIMUM_RATINGS)
    
    # Adjust confidence based on completion rate
    # Higher completion rates increase confidence in the score
    completion_factor = completion_rate * 0.5 + 0.5  # Ranges from 0.5 to 1.0
    adjusted_confidence = rating_confidence * completion_factor
    
    # Calculate engagement score (how many people actually rate after adding)
    engagement_bonus = math.log10(score_given + 1) * completion_rate * 0.1
    
    # Popularity bonus considering both ratings and total interest
    # Weighted more heavily toward actual ratings
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
    
    # Compile metrics for analysis
    metrics = {
        "ptw_count": ptw_count,
        "completion_rate": completion_rate * 100,
        "confidence": adjusted_confidence * 100,
        "engagement_bonus": engagement_bonus,
        "popularity_bonus": popularity_bonus
    }
    
    return max(1.0, min(10.0, fair_score)), metrics

# Dataset with corrected interpretation
dataset = [
    ("Monogatari S1", 61094, 8.91, 31246),
    ("Monogatari S2", 24045, 8.90, 11574),
    ("Monogatari S3", 19626, 8.83, 8321),
    ("Mushoku Tensei", 91393, 8.83, 65658),
    ("Spice and Wolf", 66209, 8.82, 32226),
    ("86", 43586, 8.82, 21175),
    ("COTE p1", 89803, 8.81, 56219),
    ("Re:Zero", 73645, 8.80, 40938),
    ("Honzuki no Gekokujou", 16766, 8.78, 9523),
    ("COTE p2", 38809, 8.78, 24946)
]

# Calculate rankings with detailed metrics
print("\nDetailed Ranking Analysis:\n")
print(f"{'Old Rank':<9} {'Title':<20} {'Total':>8} {'Completed':>9} {'PTW':>8} {'Completion%':>11} {'Score':>7} {'Fair Score':>11} {'New Rank':>10}")
print("-" * 100)

results = []
for i, (title, total, mean_score, completed) in enumerate(dataset, 1):
    popularity_rank = sorted(dataset, key=lambda x: x[1], reverse=True).index((title, total, mean_score, completed))
    fair_score, metrics = calculate_fair_score(total, completed, mean_score, popularity_rank + 1)
    results.append((i, title, total, completed, mean_score, fair_score, metrics))

# Sort by fair score
results.sort(key=lambda x: x[5], reverse=True)

for old_rank, (old_rank, title, total, completed, mean_score, fair_score, metrics) in enumerate(results, 1):
    new_rank = next(i for i, r in enumerate(results, 1) if r[0] == old_rank)
    rank_change = old_rank - new_rank
    rank_indicator = f"{new_rank} ({'=' if rank_change == 0 else f'+{rank_change}' if rank_change > 0 else str(rank_change)})"
    
    print(f"{old_rank:<9} {title:<20} {total:>8} {completed:>9} {metrics['ptw_count']:>8} {metrics['completion_rate']:>10.1f}% {mean_score:>7.2f} {fair_score:>11.2f} {rank_indicator:>10}")
