import math
from typing import Dict, Tuple

def calculate_fair_score(total_ratings: int, mean_score: float, popularity_rank: int) -> float:
    MINIMUM_RATINGS = 100   # Reduced minimum ratings threshold
    BAYESIAN_PRIOR = 7.0    # Prior score (global mean across MAL)
    PRIOR_WEIGHT = 500      # Weight of the prior
    
    # Estimate potential plan-to-watch impact
    estimated_ptw_ratio = (mean_score / 10) * 0.5
    potential_ptw = total_ratings * estimated_ptw_ratio
    
    # Adjust confidence based on potential hidden PTW numbers
    adjusted_total = total_ratings + potential_ptw
    confidence = min(1.0, (total_ratings / MINIMUM_RATINGS) * (1 - estimated_ptw_ratio))
    
    # Calculate popularity bonus with PTW consideration
    popularity_bonus = math.log10(adjusted_total + 1) * 0.08
    
    # Add small bonus for shows that convert PTW to actual ratings
    completion_bonus = math.log10(total_ratings / (popularity_rank + 1)) * 0.05
    
    # Combine Bayesian estimate with adjusted factors
    bayesian_score = (
        (PRIOR_WEIGHT * BAYESIAN_PRIOR + total_ratings * mean_score) /
        (PRIOR_WEIGHT + total_ratings)
    )
    
    # Final score calculation with all adjustments
    fair_score = (bayesian_score * confidence) + popularity_bonus + completion_bonus
    
    # Ensure score stays within 1-10 range
    return max(1.0, min(10.0, fair_score))

# Dataset with titles
dataset = [
    (1, "Monogatari S1", 61094, 8.91),
    (2, "Monogatari S2", 24045, 8.90),
    (3, "Monogatari S3", 19626, 8.83),
    (4, "Mushoku Tensei", 91393, 8.83),
    (5, "Spice and Wolf", 66209, 8.82),
    (6, "86", 43586, 8.82),
    (7, "COTE p1", 89803, 8.81),
    (8, "Re:Zero", 73645, 8.80),
    (9, "Honzuki no Gekokujou", 16766, 8.78),
    (10, "COTE p2", 38809, 8.78)
]

print("\nRanking Analysis with Lower Minimum Ratings (100):\n")
print(f"{'Old Rank':<9} {'Title':<20} {'Ratings':>8} {'Score':>7} {'Est. PTW%':>10} {'Fair Score':>11} {'New Rank':>10}")
print("-" * 80)

# Calculate fair scores and store results
results = []
for rank, title, ratings, mean_score in dataset:
    popularity_rank = sorted(dataset, key=lambda x: x[2], reverse=True).index((rank, title, ratings, mean_score))
    fair_score = calculate_fair_score(ratings, mean_score, popularity_rank + 1)
    estimated_ptw = (mean_score / 10) * 0.5 * 100
    results.append((rank, title, ratings, mean_score, estimated_ptw, fair_score))

# Sort by fair score and display results
results.sort(key=lambda x: x[5], reverse=True)
for old_rank, title, ratings, mean_score, est_ptw, fair_score in results:
    new_rank = next(i for i, (rank, _, _, _, _, _) in enumerate(results, 1) if rank == old_rank)
    rank_change = old_rank - new_rank
    rank_indicator = f"{new_rank} ({'=' if rank_change == 0 else f'+{rank_change}' if rank_change > 0 else str(rank_change)})"
    
    print(f"{old_rank:<9} {title:<20} {ratings:>8} {mean_score:>7.2f} {est_ptw:>9.1f}% {fair_score:>11.2f} {rank_indicator:>10}")
significant_changes = [r for r in results if abs(r[0] - next(i for i, (rank, _, _, _, _, _) in enumerate(results, 1) if rank == r[0])) >= 2]
if significant_changes:
    print("\nMost Significant Rank Changes:")
    for old_rank, title, ratings, mean_score, est_ptw, fair_score in significant_changes:
        new_rank = next(i for i, (rank, _, _, _, _, _) in enumerate(results, 1) if rank == old_rank)
        rank_change = old_rank - new_rank
        direction = "up" if rank_change > 0 else "down"
        print(f"• {title} moved {direction} {abs(rank_change)} positions")
