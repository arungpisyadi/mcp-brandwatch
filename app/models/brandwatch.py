from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class BrandwatchProject(BaseModel):
    id: int
    name: str
    description: Optional[str]
    billableClientId: int
    billableClientName: str
    timezone: str
    billableClientIsPitch: bool

class BrandwatchQuery(BaseModel):
    id: int
    name: str
    type: str
    creationDate: datetime
    lastModificationDate: datetime
    lastModifiedUsername: str
    lockedQuery: bool
    lockedByUsername: Optional[str]
    languages: List[str]
    contentSources: List[str]
    languageAgnostic: bool
    booleanQuery: Optional[str]
    startDate: Optional[datetime]
    percentComplete: Optional[float]
    samplePercentage: Optional[float]
    sampled: Optional[bool]

class BrandwatchMention(BaseModel):
    id: int
    content: str
    author: str
    source: str
    timestamp: datetime
    queryId: int
    projectId: int
    language: str
    sentiment: Optional[str]
    reach: Optional[int]
    engagement: Optional[int] 