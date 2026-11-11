from typing import TypedDict

from app.models.research import CompetitorProfile
from app.models.intelligence import CompetitorIntelligence


class AgentState(TypedDict, total=False):

    profile: CompetitorProfile

    intelligence: CompetitorIntelligence

    verification_summary: dict

    errors: list[str]