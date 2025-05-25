from typing import Any, Dict, List
from app.interfaces.base import IPresenter
from app.models.brandwatch import BrandwatchProject, BrandwatchQuery, BrandwatchMention

class BrandwatchPresenter(IPresenter):
    def transform_data(self, data: Any) -> Dict[str, Any]:
        if isinstance(data, BrandwatchProject):
            return self.transform_project_data(data)
        elif isinstance(data, BrandwatchQuery):
            return self.transform_query_data(data)
        elif isinstance(data, BrandwatchMention):
            return self.transform_mention_data(data)
        raise ValueError("Unsupported data type")

    def transform_project_data(self, data: BrandwatchProject) -> Dict[str, Any]:
        return {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "client": {
                "id": data.billableClientId,
                "name": data.billableClientName,
                "is_pitch": data.billableClientIsPitch
            },
            "timezone": data.timezone
        }

    def transform_query_data(self, data: BrandwatchQuery) -> Dict[str, Any]:
        return {
            "id": data.id,
            "name": data.name,
            "type": data.type,
            "created_at": data.creationDate.isoformat(),
            "modified_at": data.lastModificationDate.isoformat(),
            "modified_by": data.lastModifiedUsername,
            "status": {
                "locked": data.lockedQuery,
                "locked_by": data.lockedByUsername
            },
            "settings": {
                "languages": data.languages,
                "content_sources": data.contentSources,
                "language_agnostic": data.languageAgnostic
            },
            "query": {
                "boolean": data.booleanQuery,
                "start_date": data.startDate.isoformat() if data.startDate else None,
                "completion": {
                    "percent": data.percentComplete,
                    "sample_percentage": data.samplePercentage,
                    "sampled": data.sampled
                }
            }
        }

    def transform_mention_data(self, data: BrandwatchMention) -> Dict[str, Any]:
        return {
            "id": data.id,
            "content": data.content,
            "author": data.author,
            "source": data.source,
            "timestamp": data.timestamp.isoformat(),
            "metadata": {
                "query_id": data.queryId,
                "project_id": data.projectId,
                "language": data.language,
                "sentiment": data.sentiment,
                "metrics": {
                    "reach": data.reach,
                    "engagement": data.engagement
                }
            }
        }

    def transform_list(self, items: List[Any]) -> List[Dict[str, Any]]:
        return [self.transform_data(item) for item in items] 