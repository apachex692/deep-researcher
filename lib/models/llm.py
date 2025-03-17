from dataclasses import dataclass
from math import ceil

from pydantic import BaseModel, Field

from lib.log import logger


class SERPQuery(BaseModel):
    query: str = Field(..., title="SERP Query")
    research_goal: str = Field(
        ...,
        title="Research Goal",
        description=(
            "First, talk about the goal of the research that this query is "
            "meant to accomplish. Then, go deeper into how to advance the "
            "research once the results are found, mentioning additional "
            "research directions. Be as specific as possible, especially for "
            "additional research directions."
        ),
    )


class SERPQueries(BaseModel):
    queries: list[SERPQuery] = Field(..., title="List of SERP Queries")


class UserQueryRefinementQuestions(BaseModel):
    questions: list[str] = Field(
        ...,
        title="List of User Query Refinement Questions",
        description=("Follow up questions to clarify the research direction."),
    )


class Learning(BaseModel):
    learning: str = Field(
        ...,
        title="Learnings from Data",
        description=(
            "Generate a concise, data-driven insight from SERP "
            "analysis. Provide actionable, specific information highlighting "
            "key patterns or trends. Ensure insights are evidence-based with "
            "high signal-to-noise ratio to inform decisions or research."
        ),
    )
    follow_up_queries: list[str] = Field(
        ...,
        title="Follow-up Queries",
        description=(
            "Curated, insightful queries to deepen topic understanding. "
            "Questions should guide further research, uncover insights, or "
            "validate hypotheses. Each should be clear, specific, and "
            "data-aligned to ensure efficient and impactful subsequent "
            "investigations."
        ),
    )


@dataclass
class DeepResearchHyperParameters:
    num_refinement_questions: int
    num_learnings: int

    learning_width: int
    _learning_depth: int

    @property
    def max_allowed_depth(self) -> int:
        return ceil(self.learning_width / 2)

    @property
    def learning_depth(self) -> int:
        return self._learning_depth

    @learning_depth.setter
    def learning_depth(self, depth: int) -> None:
        max_allowed_depth = self.max_allowed_depth

        if depth > max_allowed_depth:
            logger.warning(
                "Depth %d Exceeded for Width %d (capping to: %d)",
                depth,
                self.learning_width,
                max_allowed_depth,
            )
            self._learning_depth = max_allowed_depth
        else:
            self._learning_depth = depth

    def __init__(
        self,
        num_refinement_questions: int,
        num_learnings: int,
        learning_width: int,
        learning_depth: int,
    ):
        self.num_refinement_questions = num_refinement_questions
        self.num_learnings = num_learnings
        self.learning_width = learning_width
        self.learning_depth = learning_depth

    def __repr__(self):
        return (
            f"DeepResearchHyperParameters("
            f"num_refinement_questions={self.num_refinement_questions}, "
            f"num_learnings={self.num_learnings}, "
            f"learning_width={self.learning_width}, "
            f"learning_depth={self.learning_depth})"
        )

    def calculate_width_for_depth(self, depth: int) -> int:
        return ceil(self.learning_width / 2**depth)
