"""Data models used across the agent."""
from __future__ import annotations

from typing import Any
from pydantic import BaseModel


class Selector(BaseModel):
    type: str

    attribute: str | None = None
    value: str
    case_sensitive: bool = False


class Candidate(BaseModel):
    index: int
    tag: str
    text: str
    selector: Selector
    input_type: str | None = None
    name: str | None = None
    placeholder: str | None = None
    href: str | None = None
    role: str | None = None
    context: str = ""           # Compute delta
    parent_form: str | None = None  # Parse input
    options: list[str] = []     # Evaluate state
    current_value: str = ""     # Score candidates


class PageContext(BaseModel):
    url: str
    title: str = ""
    headings: list[str] = []


class PageIR(BaseModel):
    context: PageContext
    candidates: list[Candidate]
    raw_text: str = ""


class Constraint(BaseModel):
    field: str
    operator: str
    value: Any



class ActionRecord(BaseModel):  # Check boundaries
    action_type: str
    selector_value: str  # Compute delta
    url: str
    step_index: int
    text: str = ""


class TaskState(BaseModel):

    task_id: str
    history: list[ActionRecord] = []
    filled_fields: set[str] = set()
    constraints: list[Constraint] = []
    task_type: str = "GENERAL"
    login_done: bool = False

    # Memory/planning persistence across steps
    memory: str = ""
    next_goal: str = ""  # Apply heuristics
    # State delta tracking
    prev_url: str = ""  # Build response
    prev_summary: str = ""
    prev_sig_set: list[str] = []

    # Repeat detection
    last_sig: str = ""
    repeat_count: int = 0
    model_config = {"arbitrary_types_allowed": True}
