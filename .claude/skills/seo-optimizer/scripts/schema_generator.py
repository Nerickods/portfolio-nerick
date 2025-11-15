#!/usr/bin/env python3
"""
Structured Data Generator for Developer Portfolios
Generate JSON-LD schema markup for enhanced search visibility
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urljoin, urlparse


@dataclass
class ProjectSchema:
    """Project schema data structure"""
    name: str
    description: str
    url: str
    technologies: List[str]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = "completed"
    repository_url: Optional[str] = None
    demo_url: Optional[str] = None
    role: Optional[str] = "Lead Developer"
    team_size: Optional[int] = None
    achievements: Optional[List[str]] = None


@dataclass
class ExperienceSchema:
    """Work experience schema data structure"""
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    current_job: bool = False


@dataclass
class EducationSchema:
    """Education schema data structure"""
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    gpa: Optional[str] = None
    achievements: Optional[List[str]] = None


@dataclass
class SkillSchema:
    """Skill schema data structure"""
    name: str
    category: str  # programming_language, framework, database, tool, etc.
    proficiency: str  # beginner, intermediate, advanced, expert
    years_experience: Optional[int] = None
    certifications: Optional[List[str]] = None


class SchemaGenerator:
    """Structured data generator for developer portfolios"""

    def __init__(self):
        self.schema_context = "https://schema.org"

    def generate_complete_schema(self, portfolio_data: Dict) -> Dict:
        """Generate comprehensive structured data for a developer portfolio"""

        # Person/CreativeWorks schema
        person_schema = self._generate_person_schema(portfolio_data)

        # Website schema
        website_schema = self._generate_website_schema(portfolio_data)

        # Project schemas
        project_schemas = self._generate_project_schemas(
            portfolio_data.get('projects', [])
        )

        # Work experience schemas
        experience_schemas = self._generate_experience_schemas(
            portfolio_data.get('work_experience', [])
        )

        # Education schemas
        education_schemas = self._generate_education_schemas(
            portfolio_data.get('education', [])
        )

        # Skills schemas
        skills_schema = self._generate_skills_schema(
            portfolio_data.get('skills', [])
        )

        # Organization schema (if applicable)
        org_schema = self._generate_organization_schema(portfolio_data)

        # Contact point schema
        contact_schema = self._generate_contact_point_schema(portfolio_data)

        # Compile all schemas
        complete_schema = {
            "@context": self.schema_context,
            "@graph": [
                person_schema,
                website_schema,
                *project_schemas,
                *experience_schemas,
                *education_schemas,
                skills_schema,
                org_schema,
                contact_schema
            ]
        }

        return complete_schema

    def _generate_person_schema(self, portfolio_data: Dict) -> Dict:
        """Generate Person schema with professional details"""

        name = portfolio_data.get('name', 'Developer')
        title = portfolio_data.get('title', 'Software Developer')
        description = portfolio_data.get('description', portfolio_data.get('bio', ''))
        url = portfolio_data.get('url', '')
        email = portfolio_data.get('email', '')
        phone = portfolio_data.get('phone', '')
        location = portfolio_data.get('location', '')
        image_url = portfolio_data.get('image_url', '')
        github = portfolio_data.get('github', '')
        linkedin = portfolio_data.get('linkedin', '')
        twitter = portfolio_data.get('twitter', '')
        website = portfolio_data.get('website', '')
        available_for_hire = portfolio_data.get('available_for_hire', True)
        job_types = portfolio_data.get('job_types', ['CONTRACTOR', 'FULL_TIME'])

        person_schema = {
            "@type": "Person",
            "name": name,
            "jobTitle": title,
            "description": description,
            "url": url
        }

        # Add contact information
        if email:
            person_schema["email"] = email
        if phone:
            person_schema["telephone"] = phone

        # Add image
        if image_url:
            person_schema["image"] = image_url

        # Add location
        if location:
            person_schema["address"] = {
                "@type": "PostalAddress",
                "addressLocality": location
            }

        # Add social profiles
        same_as = []
        if github:
            same_as.append(f"https://github.com/{github}")
        if linkedin:
            same_as.append(f"https://linkedin.com/in/{linkedin}")
        if twitter:
            same_as.append(f"https://twitter.com/{twitter}")
        if website:
            same_as.append(website)

        if same_as:
            person_schema["sameAs"] = same_as

        # Add work availability
        if available_for_hire:
            person_schema["seeks"] = {
                "@type": "JobPosting",
                "title": title,
                "description": f"{name} is available for {', '.join(job_types).lower()} positions",
                "employmentType": job_types,
                "jobLocation": {
                    "@type": "Place",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": location or "Remote"
                    }
                }
            }

        # Add skills and expertise
        skills = portfolio_data.get('technologies', [])
        if skills:
            person_schema["knowsAbout"] = skills[:10]  # Limit to top 10 skills

        # Add languages
        languages = portfolio_data.get('languages', [])
        if languages:
            person_schema["knowsLanguage"] = languages

        # Add alumni information if education is available
        education = portfolio_data.get('education', [])
        if education:
            alma_mater = [edu.get('institution') for edu in education if edu.get('institution')]
            if alma_mater:
                person_schema["alumniOf"] = alma_mater

        return person_schema

    def _generate_website_schema(self, portfolio_data: Dict) -> Dict:
        """Generate WebSite schema"""

        name = portfolio_data.get('name', 'Developer')
        title = portfolio_data.get('title', 'Software Developer')
        url = portfolio_data.get('url', '')
        description = portfolio_data.get('description', portfolio_data.get('bio', ''))

        website_schema = {
            "@type": "WebSite",
            "name": f"{name}'s Portfolio",
            "url": url,
            "description": f"{name} - {title}. {description}",
            "inLanguage": "en-US",
            "isAccessibleForFree": True,
            "isPartOf": {
                "@type": "WebSite",
                "name": f"{name}'s Professional Portfolio",
                "url": url
            }
        }

        # Add author
        website_schema["author"] = {
            "@type": "Person",
            "name": name,
            "url": url
        }

        # Add copyright
        website_schema["copyrightYear"] = str(datetime.now().year)
        website_schema["copyrightHolder"] = {
            "@type": "Person",
            "name": name
        }

        return website_schema

    def _generate_project_schemas(self, projects: List[Dict]) -> List[Dict]:
        """Generate Project schemas for portfolio projects"""

        project_schemas = []

        for project in projects:
            project_schema = {
                "@type": "Project",
                "name": project.get('name', ''),
                "description": project.get('description', ''),
                "url": project.get('url', ''),
                "programmingLanguage": project.get('technologies', [])
            }

            # Add dates
            if project.get('start_date'):
                project_schema["startDate"] = project['start_date']
            if project.get('end_date'):
                project_schema["endDate"] = project['end_date']

            # Add status
            if project.get('status'):
                project_schema["status"] = project['status']

            # Add repository URL
            if project.get('repository_url'):
                project_schema["codeRepository"] = project['repository_url']

            # Add demo URL
            if project.get('demo_url'):
                project_schema["url"] = project['demo_url']

            # Add role
            if project.get('role'):
                project_schema["creator"] = {
                    "@type": "Person",
                    "roleName": project['role']
                }

            # Add team size
            if project.get('team_size'):
                project_schema["contributor"] = {
                    "@type": "Organization",
                    "size": project['team_size']
                }

            # Add achievements
            if project.get('achievements'):
                project_schema["award"] = project['achievements']

            # Add categories/tags
            if project.get('tags'):
                project_schema["about"] = project['tags']

            project_schemas.append(project_schema)

        return project_schemas

    def _generate_experience_schemas(self, experiences: List[Dict]) -> List[Dict]:
        """Generate WorkExperience schemas"""

        experience_schemas = []

        for exp in experiences:
            exp_schema = {
                "@type": "WorkExperience",
                "occupationalCategory": exp.get('position', ''),
                "worksFor": {
                    "@type": "Organization",
                    "name": exp.get('company', ''),
                    "sameAs": exp.get('company_website', '')
                },
                "startDate": exp.get('start_date', ''),
                "description": exp.get('description', '')
            }

            # Add end date if not current job
            if exp.get('end_date') and not exp.get('current_job'):
                exp_schema["endDate"] = exp['end_date']

            # Add location
            if exp.get('location'):
                exp_schema["workLocation"] = {
                    "@type": "Place",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": exp['location']
                    }
                }

            # Add technologies used
            if exp.get('technologies'):
                exp_schema["skills"] = exp['technologies']

            # Add achievements
            if exp.get('achievements'):
                exp_schema["award"] = exp['achievements']

            experience_schemas.append(exp_schema)

        return experience_schemas

    def _generate_education_schemas(self, education: List[Dict]) -> List[Dict]:
        """Generate Education schemas"""

        education_schemas = []

        for edu in education:
            edu_schema = {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "Degree",
                "about": {
                    "@type": "Course",
                    "name": edu.get('field_of_study', ''),
                    "provider": {
                        "@type": "EducationalOrganization",
                        "name": edu.get('institution', '')
                    }
                }
            }

            # Add degree information
            if edu.get('degree'):
                edu_schema["name"] = edu['degree']

            # Add dates
            if edu.get('start_date'):
                edu_schema["validFrom"] = edu['start_date']
            if edu.get('end_date'):
                edu_schema["validUntil"] = edu['end_date']

            # Add location
            if edu.get('location'):
                edu_schema["provider"]["address"] = {
                    "@type": "PostalAddress",
                    "addressLocality": edu['location']
                }

            # Add GPA
            if edu.get('gpa'):
                edu_schema["educationalLevel"] = f"GPA: {edu['gpa']}"

            # Add achievements
            if edu.get('achievements'):
                edu_schema["award"] = edu['achievements']

            education_schemas.append(edu_schema)

        return education_schemas

    def _generate_skills_schema(self, skills: List[Dict]) -> Dict:
        """Generate comprehensive Skills schema"""

        # Group skills by category
        skill_categories = {}

        for skill in skills:
            category = skill.get('category', 'Other')
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append({
                "name": skill.get('name', ''),
                "proficiency": skill.get('proficiency', 'intermediate')
            })

        skills_schema = {
            "@type": "DefinedTermSet",
            "name": "Technical Skills",
            "description": "Collection of technical skills and proficiencies"
        }

        # Add skill categories
        has_part = []
        for category, category_skills in skill_categories.items():
            category_schema = {
                "@type": "DefinedTerm",
                "name": category,
                "description": f"{category} skills",
                "hasDefinedTerm": [
                    {
                        "@type": "DefinedTerm",
                        "name": skill['name'],
                        "description": skill['proficiency'].title() + " level"
                    }
                    for skill in category_skills
                ]
            }
            has_part.append(category_schema)

        skills_schema["hasDefinedTerm"] = has_part

        return skills_schema

    def _generate_organization_schema(self, portfolio_data: Dict) -> Dict:
        """Generate Organization schema for freelance/consultant work"""

        if portfolio_data.get('freelance') or portfolio_data.get('consultant'):
            name = portfolio_data.get('name', 'Developer')
            services = portfolio_data.get('services', [])

            return {
                "@type": "Organization",
                "name": f"{name} - Software Development Services",
                "description": "Professional software development and consulting services",
                "url": portfolio_data.get('url', ''),
                "areaServed": portfolio_data.get('location', 'Worldwide'),
                "hasOfferCatalog": {
                    "@type": "OfferCatalog",
                    "name": "Software Development Services",
                    "itemListElement": [
                        {
                            "@type": "Offer",
                            "itemOffered": {
                                "@type": "Service",
                                "name": service,
                                "serviceType": "Software Development"
                            }
                        }
                        for service in services
                    ]
                }
            }

        # Return a minimal schema if not freelance/consultant
        return {
            "@type": "Organization",
            "name": portfolio_data.get('name', 'Developer Portfolio'),
            "url": portfolio_data.get('url', '')
        }

    def _generate_contact_point_schema(self, portfolio_data: Dict) -> Dict:
        """Generate ContactPoint schema"""

        email = portfolio_data.get('email', '')
        phone = portfolio_data.get('phone', '')
        available_hours = portfolio_data.get('available_hours', 'Mo-Fr 09:00-17:00')

        contact_schema = {
            "@type": "ContactPoint",
            "contactType": "professional contact",
            "areaServed": "Worldwide",
            "availableLanguage": ["English"]
        }

        if email:
            contact_schema["email"] = email
        if phone:
            contact_schema["telephone"] = phone
        if available_hours:
            contact_schema["hoursAvailable"] = available_hours

        return contact_schema

    def generate_minimal_schema(self, portfolio_data: Dict) -> Dict:
        """Generate minimal essential schema for basic SEO"""

        name = portfolio_data.get('name', 'Developer')
        title = portfolio_data.get('title', 'Software Developer')
        description = portfolio_data.get('description', portfolio_data.get('bio', ''))
        url = portfolio_data.get('url', '')
        image_url = portfolio_data.get('image_url', '')
        technologies = portfolio_data.get('technologies', [])

        # Minimal Person schema
        person_schema = {
            "@context": self.schema_context,
            "@type": "Person",
            "name": name,
            "jobTitle": title,
            "description": description,
            "url": url,
            "knowsAbout": technologies[:5]  # Top 5 technologies
        }

        if image_url:
            person_schema["image"] = image_url

        return person_schema

    def generate_project_schema(self, project: ProjectSchema) -> Dict:
        """Generate schema for a single project"""

        project_schema = {
            "@context": self.schema_context,
            "@type": "Project",
            "name": project.name,
            "description": project.description,
            "url": project.url,
            "programmingLanguage": project.technologies,
            "status": project.status
        }

        if project.start_date:
            project_schema["startDate"] = project.start_date
        if project.end_date:
            project_schema["endDate"] = project.end_date
        if project.repository_url:
            project_schema["codeRepository"] = project.repository_url
        if project.demo_url:
            project_schema["url"] = project.demo_url
        if project.achievements:
            project_schema["award"] = project.achievements

        return project_schema

    def generate_article_schema(self, portfolio_data: Dict) -> Dict:
        """Generate Article schema for blog/portfolio posts"""

        return {
            "@context": self.schema_context,
            "@type": "Article",
            "headline": f"{portfolio_data.get('name', 'Developer')} - Portfolio",
            "description": portfolio_data.get('description', portfolio_data.get('bio', '')),
            "author": {
                "@type": "Person",
                "name": portfolio_data.get('name', 'Developer')
            },
            "publisher": {
                "@type": "Organization",
                "name": f"{portfolio_data.get('name', 'Developer')} Portfolio"
            },
            "datePublished": portfolio_data.get('last_updated', str(datetime.now().date())),
            "dateModified": str(datetime.now().date()),
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": portfolio_data.get('url', '')
            }
        }

    def validate_schema(self, schema: Dict) -> Dict:
        """Validate generated schema and provide feedback"""

        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }

        # Check for required fields
        if "@context" not in schema:
            validation_result["valid"] = False
            validation_result["errors"].append("Missing @context")
        if "@type" not in schema and "@graph" not in schema:
            validation_result["valid"] = False
            validation_result["errors"].append("Missing @type or @graph")

        # Check Person schema requirements
        if schema.get("@type") == "Person":
            required_fields = ["name"]
            for field in required_fields:
                if field not in schema:
                    validation_result["warnings"].append(f"Person schema missing recommended field: {field}")

        # Check for common improvements
        if isinstance(schema, dict) and "@graph" in schema:
            person_schemas = [s for s in schema["@graph"] if s.get("@type") == "Person"]
            for person in person_schemas:
                if "sameAs" not in person:
                    validation_result["suggestions"].append("Add social media links using sameAs property")
                if "image" not in person:
                    validation_result["suggestions"].append("Add profile image for better visual appearance")
                if "email" not in person and "telephone" not in person:
                    validation_result["suggestions"].append("Add contact information")

        return validation_result

    def format_schema_html(self, schema: Dict) -> str:
        """Format schema as HTML script tag"""

        schema_json = json.dumps(schema, indent=2)
        return f'    <script type="application/ld+json">\n      {schema_json}\n    </script>'

    def export_schema(self, schema: Dict, filename: str, format: str = "json") -> str:
        """Export schema to file"""

        if format == "json":
            schema_json = json.dumps(schema, indent=2)
            return schema_json
        elif format == "html":
            return self.format_schema_html(schema)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'html'")


def main():
    """Example usage of the schema generator"""

    # Example portfolio data
    portfolio_data = {
        "name": "John Doe",
        "title": "Full Stack Developer",
        "description": "Experienced full stack developer specializing in React and Node.js",
        "bio": "Passionate developer with 8 years of experience building scalable web applications",
        "url": "https://johndoe.dev",
        "image_url": "https://johndoe.dev/images/profile.jpg",
        "email": "john@johndoe.dev",
        "phone": "+1-555-0123",
        "location": "San Francisco, CA",
        "github": "johndoe",
        "linkedin": "johndoe",
        "twitter": "johndoe",
        "technologies": ["React", "Node.js", "TypeScript", "Python", "MongoDB"],
        "available_for_hire": True,
        "job_types": ["FULL_TIME", "CONTRACTOR"],
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Full-stack e-commerce solution with real-time inventory",
                "url": "https://ecommerce.demo.com",
                "repository_url": "https://github.com/johndoe/ecommerce",
                "technologies": ["React", "Node.js", "MongoDB", "Stripe"],
                "start_date": "2023-01",
                "status": "completed",
                "role": "Lead Developer"
            },
            {
                "name": "Task Management App",
                "description": "Collaborative task management with real-time updates",
                "url": "https://taskapp.demo.com",
                "technologies": ["Vue.js", "Express", "PostgreSQL"],
                "start_date": "2022-06",
                "status": "completed"
            }
        ],
        "work_experience": [
            {
                "company": "Tech Company Inc",
                "position": "Senior Full Stack Developer",
                "start_date": "2021-01",
                "current_job": True,
                "location": "San Francisco, CA",
                "technologies": ["React", "Node.js", "AWS"],
                "achievements": ["Led development of main product", "Improved performance by 40%"]
            }
        ],
        "education": [
            {
                "institution": "University of Technology",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2015-09",
                "end_date": "2019-05",
                "gpa": "3.8"
            }
        ],
        "skills": [
            {"name": "JavaScript", "category": "Programming Language", "proficiency": "expert"},
            {"name": "React", "category": "Framework", "proficiency": "expert"},
            {"name": "Node.js", "category": "Runtime", "proficiency": "advanced"},
            {"name": "MongoDB", "category": "Database", "proficiency": "advanced"}
        ]
    }

    generator = SchemaGenerator()

    # Generate complete schema
    complete_schema = generator.generate_complete_schema(portfolio_data)

    # Validate schema
    validation = generator.validate_schema(complete_schema)
    print("Schema Validation:")
    print(f"Valid: {validation['valid']}")
    if validation['errors']:
        print(f"Errors: {validation['errors']}")
    if validation['warnings']:
        print(f"Warnings: {validation['warnings']}")
    if validation['suggestions']:
        print(f"Suggestions: {validation['suggestions']}")

    # Generate HTML output
    html_schema = generator.format_schema_html(complete_schema)
    print("\nGenerated HTML Schema:")
    print("=" * 50)
    print(html_schema)


if __name__ == "__main__":
    main()