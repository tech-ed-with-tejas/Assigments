from typing import List, Optional
from pydantic import BaseModel

class JobMeta(BaseModel):
    title: Optional[str]
    level: Optional[str]
    employment_type: Optional[str]  # Full-time, Contract, Internship, etc.
    location: Optional[str]
    remote_policy: Optional[str]    # Remote, Hybrid, On-site
    relocation_required: Optional[bool]
    travel_requirements: Optional[str]

class JobRequirements(BaseModel):
    required_skills: Optional[List[str]]
    preferred_skills: Optional[List[str]]
    years_of_experience: Optional[str]
    required_qualifications: Optional[List[str]]
    preferred_qualifications: Optional[List[str]]
    eligibility: Optional[str]  # Work authorization or visa info

class JobCompensation(BaseModel):
    salary_range: Optional[str]
    benefits: Optional[List[str]]
    equity: Optional[bool]

class JobPostingDetails(BaseModel):
    posted_date: Optional[str]
    application_deadline: Optional[str]
    company_overview: Optional[str]
    department: Optional[str]

class JobDescription(BaseModel):
    meta: Optional[JobMeta]
    responsibilities: Optional[List[str]]
    day_to_day_tasks: Optional[List[str]]
    requirements: Optional[JobRequirements]
    compensation: Optional[JobCompensation]
    posting_details: Optional[JobPostingDetails]
    culture: Optional[str]
    growth_opportunities: Optional[str]
    diversity_statement: Optional[str]
    kpis: Optional[List[str]]


from pydantic import BaseModel,  Field

class ContactInformation(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: str = Field(..., description="Primary contact email address")
    phone: str = Field(..., description="Primary phone number")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Personal portfolio website")
    address: Optional[str] = Field(None, description="Full residential address")

class WorkExperience(BaseModel):
    job_title: str = Field(..., description="Job title held at the company")
    company: str = Field(..., description="Name of the company/organization")
    location: Optional[str] = Field(None, description="Location of the company")
    start_date: str = Field(..., description="Start date of employment (YYYY-MM format recommended)")
    end_date: Optional[str] = Field(None, description="End date of employment (or 'Present' if ongoing)")
    responsibilities: Optional[List[str]] = Field(None, description="List of key responsibilities")
    achievements: Optional[List[str]] = Field(None, description="Key achievements or accomplishments")
    reference_link: Optional[str] = Field(None, description="Optional link to company profile or verification")

class Education(BaseModel):
    degree: str = Field(..., description="Degree earned (e.g., B.Sc., M.Sc.)")
    institution: str = Field(..., description="Name of the educational institution")
    graduation_year: str = Field(..., description="Graduation year")
    gpa: Optional[str] = Field(None, description="Grade Point Average (if applicable)")
    coursework: Optional[List[str]] = Field(None, description="Relevant coursework for freshers/students")
    transcript_link: Optional[str] = Field(None, description="Link to academic transcript (if available)")

class Project(BaseModel):
    title: str = Field(..., description="Title of the project")
    description: Optional[str] = Field(None, description="Brief description of the project")
    technologies_used: Optional[List[str]] = Field(None, description="Technologies or tools used in the project")
    project_link: Optional[str] = Field(None, description="Link to project demo, GitHub, or portfolio")

class ResearchPaper(BaseModel):
    title: str = Field(..., description="Title of the research paper")
    publication_link: Optional[str] = Field(None, description="Link to the published paper")
    conference_or_journal: Optional[str] = Field(None, description="Name of conference or journal")
    publication_date: Optional[str] = Field(None, description="Publication date (YYYY-MM format)")
    abstract: Optional[str] = Field(None, description="Brief abstract or summary")
    co_authors: Optional[List[str]] = Field(None, description="List of co-authors")

class Patent(BaseModel):
    title: str = Field(..., description="Patent title")
    patent_number: Optional[str] = Field(None, description="Patent number or reference")
    patent_link: Optional[str] = Field(None, description="Link to patent record")
    filing_date: Optional[str] = Field(None, description="Filing date (YYYY-MM format)")
    status: Optional[str] = Field(None, description="Patent status (e.g., Granted, Pending)")

class Resume(BaseModel):
    contact_information: ContactInformation = Field(..., description="Candidate's primary contact details")
    professional_summary: Optional[str] = Field(None, description="Short professional summary or career objective")
    skills: Optional[List[str]] = Field(None, description="List of key technical and soft skills")
    work_experience: Optional[List[WorkExperience]] = Field(None, description="Employment history")
    education: Optional[List[Education]] = Field(None, description="Educational qualifications")
    certifications: Optional[List[str]] = Field(None, description="Relevant certifications or training")
    projects: Optional[List[Project]] = Field(None, description="Notable projects completed")
    research_papers: Optional[List[ResearchPaper]] = Field(None, description="Published research papers")
    patents: Optional[List[Patent]] = Field(None, description="Patents filed or granted")
    awards: Optional[List[str]] = Field(None, description="Awards or honors received")
    volunteer_experience: Optional[List[str]] = Field(None, description="Volunteer or community work")
    publications: Optional[List[str]] = Field(None, description="Other publications (not research papers)")
    languages: Optional[List[str]] = Field(None, description="Languages known")
    hobbies: Optional[List[str]] = Field(None, description="Hobbies and interests (if relevant)")
    references: Optional[List[str]] = Field(None, description="Professional references or recommendations")
    online_presence: Optional[List[str]] = Field(None, description="Additional online profiles")
    portfolio_links: Optional[List[str]] = Field(None, description="Portfolio or design-related links")
    additional_information: Optional[str] = Field(None, description="Any other relevant information")


class SkillMatchDetail(BaseModel):
    skill: str = Field(..., description="The skill being evaluated")
    found: bool = Field(..., description="Whether the skill is present in the resume")
    match_percentage: float = Field(..., ge=0, le=100, description="How well this skill matches (%)")

class CategoryVisualization(BaseModel):
    category_name: str
    score_percentage: float = Field(..., ge=0, le=100, description="Score for this category in percentage")
    weight: float = Field(..., ge=0, le=100, description="Weight of this category in total ATS")
    reasoning: str = Field(..., description="Why this score was given")

class ATSVisualizationScore(BaseModel):
    skills: List[SkillMatchDetail] = Field(..., description="Detailed skill match breakdown")
    category_scores: List[CategoryVisualization] = Field(..., description="List of category scores with weights")
    missing_skills: List[str] = Field(default_factory=list, description="Expected skills not found in resume")
    total_score: float = Field(..., ge=0, le=100, description="Overall ATS score (%)")


