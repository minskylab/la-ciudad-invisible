from dataclasses import dataclass
from typing import List


@dataclass
class CleanPost:
    id: str
    date: str
    hashtags: List[str]
    mentions: List[str]
    image_uri: str
    likes: int
    comments: int
    relevance: float
    description: str
    comments_content: List[str]
