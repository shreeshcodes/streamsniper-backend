def calculate_viral_score(views: int, likes: int, comments: int) -> float:
    views_score = min(views / 10000, 50)
    likes_score = min(likes / 1000, 30)
    comments_score = min(comments / 100, 20)
    viral_score = views_score + likes_score + comments_score
    return min(round(viral_score, 2), 100)
