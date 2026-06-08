"""
Intelligent Resume Analyzer
"""

import os
import json
import re
from typing import List, Dict, Tuple

try:
    from fuzzywuzzy import fuzz
except ImportError:
    class fuzz:
        @staticmethod
        def ratio(s1: str, s2: str) -> int:
            return 100 if s1.lower() == s2.lower() else 0


class JobRequirement:
    """Represents a job description and its requirements."""
    def __init__(self, title: str, required_skills: List[str], min_experience: int, required_education: str):
        self.title = title
        self.required_skills = [s.lower() for s in required_skills]
        self.min_experience = min_experience
        self.required_education = required_education.lower()

class Candidate:
    """Represents a candidate parsed from a resume."""
    def __init__(self, name: str, email: str, skills: List[str], experience: int, education: str):
        self.name = name
        self.email = email
        self.skills = [s.lower() for s in skills]
        self.experience = experience
        self.education = education.lower()
        
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Candidate":
        return cls(
            name=data.get("name", "Unknown"),
            email=data.get("email", "unknown@example.com"),
            skills=data.get("skills", []),
            experience=data.get("experience", 0),
            education=data.get("education", "Unknown")
        )

class ResumeParser:
    """Handles text processing and extraction of candidate information."""
    
    @staticmethod
    def parse_text(text: str) -> Candidate:
        """Parses raw text into a Candidate object using regex."""
        try:
            name_match = re.search(r"Name:\s*(.+)", text, re.IGNORECASE)
            name = name_match.group(1).strip() if name_match else "Unknown Candidate"
            
            email_match = re.search(r"Email:\s*([\w\.-]+@[\w\.-]+)", text, re.IGNORECASE)
            email = email_match.group(1).strip() if email_match else "unknown@example.com"
            
            skills_match = re.search(r"Skills:\s*(.+)", text, re.IGNORECASE)
            skills = [s.strip() for s in skills_match.group(1).split(",")] if skills_match else []
            
            exp_match = re.search(r"Experience:\s*(\d+)\s*years?", text, re.IGNORECASE)
            experience = int(exp_match.group(1)) if exp_match else 0
            
            edu_match = re.search(r"Education:\s*(.+)", text, re.IGNORECASE)
            education = edu_match.group(1).strip() if edu_match else "Unknown Education"
            
            return Candidate(name, email, skills, experience, education)
        except Exception as e:
            print(f"Error parsing resume content: {e}")
            return Candidate("Parse Error", "", [], 0, "")

class CandidateMatcher:
    """Compares candidates with job requirements."""
    
    @staticmethod
    def match(candidate: Candidate, job: JobRequirement) -> Tuple[int, List[str], List[str]]:
        """Calculates a match score and determines matched/missing skills."""
        score = 0.0
        matched_skills = []
        missing_skills = []
        
        for req_skill in job.required_skills:
            matched = False
            for cand_skill in candidate.skills:
                match_ratio = fuzz.ratio(req_skill, cand_skill)
                if match_ratio >= 80:
                    matched = True
                    break
            
            if matched:
                matched_skills.append(req_skill)
            else:
                missing_skills.append(req_skill)
                
        if job.required_skills:
            skill_score = (len(matched_skills) / len(job.required_skills)) * 50
            score += skill_score
            
        # Experience Match (max 30 points)
        if candidate.experience >= job.min_experience:
            score += 30
        else:
            exp_ratio = min(candidate.experience / job.min_experience, 1.0)
            score += 30 * exp_ratio
            
        if job.required_education in candidate.education:
            score += 20
            
        return int(score), matched_skills, missing_skills
class ReportGenerator:
    """Generates stylized textual reports for recruiters."""
    
    @staticmethod
    def generate_text_report(candidate: Candidate, job: JobRequirement, score: int, matched_skills: List[str], missing_skills: List[str]) -> str:
        recommendation = "NOT RECOMMENDED"
        if score >= 80:
            recommendation = "STRONGLY RECOMMEND"
        elif score >= 60:
            recommendation = "RECOMMEND"
        elif score >= 40:
            recommendation = "MAYBE"
            
        report = f"""
===== CANDIDATE ANALYSIS REPORT =====
Candidate: {candidate.name} ({candidate.email})
Job: {job.title}
Match Score: {score}/100

SKILLS ANALYSIS:
• Matched ({len(matched_skills)}/{len(job.required_skills)}): {', '.join(matched_skills) if matched_skills else 'None'}
• Missing ({len(missing_skills)}/{len(job.required_skills)}): {', '.join(missing_skills) if missing_skills else 'None'}

EXPERIENCE & EDUCATION:
• Experience: {candidate.experience} years (Required: {job.min_experience}+)
• Education: {candidate.education.title()} (Required matches: '{job.required_education.title()}')

RECOMMENDATION:
{recommendation}
=====================================
"""
        return report

class DataManager:
    """Handles JSON load/save operations."""
    
    @staticmethod
    def save_candidates(candidates: List[Candidate], filename: str):
        try:
            with open(filename, 'w') as f:
                json.dump([c.to_dict() for c in candidates], f, indent=4)
            print(f"[Success] Saved {len(candidates)} candidates to {filename}")
        except IOError as e:
            print(f"[Error] Failed to save data: {e}")
            
    @staticmethod
    def load_candidates(filename: str) -> List[Candidate]:
        if not os.path.exists(filename):
            print(f"[Warning] File {filename} not found.")
            return []
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return [Candidate.from_dict(d) for d in data]
        except Exception as e:
            print(f"[Error] Failed to load data: {e}")
            return []

def main():
    print("Welcome to the Intelligent Resume Analyzer!")
    print("-" * 50)

    job = JobRequirement(
        title="Python Data Engineer",
        required_skills=["Python", "SQL", "Pandas", "ETL", "AWS"],
        min_experience=3,
        required_education="Bachelor"
    )

    raw_resume_1 = """
    Name: Alice Smith
    Email: alice.smith@example.com
    Skills: Python, sql, Machine Learning, pandas, Docker
    Experience: 4 years
    Education: Bachelor of Science in Computer Science
    """

    raw_resume_2 = """
    Name: Bob Johnson
    Email: bob.j@example.com
    Skills: Java, Spring, MySQL
    Experience: 1 years
    Education: High School Diploma
    """

    raw_resume_3 = """
    Name: Charlie Brown
    Email: charlie.b@example.com
    Skills: Python, AWS, ETL pipelines, Pandas, SQLite
    Experience: 2 years
    Education: Master in Data Science (Equivalent to Bachelor)
    """

    print("\n--> Parsing Resumes...")
    parser = ResumeParser()
    candidates = [
        parser.parse_text(raw_resume_1),
        parser.parse_text(raw_resume_2),
        parser.parse_text(raw_resume_3),
    ]

    print("\n--> Generating Reports...")
    for candidate in candidates:
        if candidate.name == "Parse Error":
            continue

        score, matched, missing = CandidateMatcher.match(candidate, job)
        report = ReportGenerator.generate_text_report(candidate, job, score, matched, missing)
        print(report)

    print("\n--> Saving candidate database to candidates.json...")
    db_file = "candidates.json"
    DataManager.save_candidates(candidates, db_file)

if __name__ == "__main__":
    main()