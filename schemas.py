from typing import List

from pydantic import BaseModel, Field


class Source(BaseModel):
    """This is the source schema used by the agent"""

    url: str = Field(description="This is the url of the source")


class AgentResponse(BaseModel):
    """This is the agent Response schema used by the agent"""

    answer: str = Field(description="This is the agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=list, description="This is the source list"
    )
