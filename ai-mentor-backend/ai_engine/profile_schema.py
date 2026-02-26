# ai_engine/profile_schema.py

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class StudentProfile:
    def __init__(
        self,
        academic_index,
        subject_scores,
        psychological_vector,
        stress_level,
        risk_level,
        budget,
        location,
        education_level
    ):
        self.academic_index = academic_index
        self.subject_scores = subject_scores
        self.psychological_vector = psychological_vector
        self.stress_level = stress_level
        self.risk_level = risk_level
        self.budget = budget
        self.location = location
        self.education_level = education_level