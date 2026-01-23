import pandas as pd
from typing import Dict

"""
Returns:
- users_posts: users with posts count
- posts_comments: posts with comments count
"""
def transform(data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    users_df = data["users"]
    posts_df = data["posts"]
    comments_df = data["comments"]

    # 1. Posts por usuário
    posts_per_user = (
        posts_df
        .groupby("userId")
        .size()
        .reset_index(name="total_posts")
    )

    users_with_posts_df = users_df.merge(
        posts_per_user,
        left_on="id",
        right_on="userId",
        how="left"
    ).drop(columns=["userId"])

    users_with_posts_df["total_posts"] = users_with_posts_df["total_posts"].fillna(0).astype(int)

    # 2. Comentários por post
    comments_per_post = (
        comments_df
        .groupby("postId")
        .reset_index(name="total_comments")
    )

    posts_with_comments_df = posts_df.merge(
        comments_per_post,
        left_on="id",
        right_on="postId",
        how="left"
    ).drop(columns=["postId"])

    posts_with_comments_df["total_comments"] = posts_with_comments_df["total_comments"].fillna(0).astype(int)

    return {
        "users_posts": users_with_posts_df,
        "posts_comments": posts_with_comments_df,
    }
