#!/usr/bin/env python3
"""
Template Engine for Portfolio Content

Provides customizable templates for different types of portfolio content
including contact emails, project summaries, and professional bios.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class PortfolioTemplateEngine:
    """Template engine for generating portfolio content with customizable styles."""

    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / "assets" / "templates"
        self.templates_dir = Path(templates_dir)
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load all available templates."""
        templates = {
            "about_me": {
                "technical": self._get_about_technical_template(),
                "business": self._get_about_business_template(),
                "casual": self._get_about_casual_template(),
                "leadership": self._get_about_leadership_template()
            },
            "contact_email": {
                "job_application": self._get_job_application_template(),
                "freelance_proposal": self._get_freelance_proposal_template(),
                "networking": self._get_networking_template(),
                "follow_up": self._get_follow_up_template(),
                "thank_you": self._get_thank_you_template()
            },
            "project_summary": {
                "technical": self._get_project_technical_template(),
                "business": self._get_project_business_template(),
                "demo": self._get_project_demo_template()
            },
            "social_media": {
                "linkedin": self._get_linkedin_template(),
                "twitter": self._get_twitter_template(),
                "github": self._get_github_template()
            }
        }
        return templates

    def generate(self, template_type: str, style: str = None, **kwargs) -> str:
        """Generate content using specified template."""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")

        template_variants = self.templates[template_type]

        if style is None:
            style = list(template_variants.keys())[0]  # Use first available style

        if style not in template_variants:
            raise ValueError(f"Unknown style '{style}' for template type '{template_type}'")

        template = template_variants[style]

        # Merge default values with provided kwargs
        context = self._get_default_context()
        context.update(kwargs)

        # Process template with context
        return self._process_template(template, context)

    def _get_default_context(self) -> Dict[str, Any]:
        """Get default context values for templates."""
        return {
            "name": "[Your Name]",
            "email": "your.email@example.com",
            "phone": "+1 (555) 123-4567",
            "linkedin": "linkedin.com/in/yourprofile",
            "github": "github.com/yourusername",
            "portfolio": "yourportfolio.com",
            "current_date": datetime.now().strftime("%B %d, %Y"),
            "years_experience": "5+",
            "title": "Senior Full-Stack Developer"
        }

    def _process_template(self, template: str, context: Dict[str, Any]) -> str:
        """Process template string with context variables."""
        processed = template

        # Simple string replacement (can be enhanced with Jinja2 or similar)
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            if isinstance(value, list):
                placeholder = f"{{{{{key}}}}}" if value else ""
                processed = processed.replace(placeholder, "\n".join(f"- {item}" for item in value) if value else "")
            elif isinstance(value, dict):
                placeholder = f"{{{{{key}}}}}"
                dict_content = []
                for k, v in value.items():
                    if v:
                        dict_content.append(f"- **{k.title()}**: {', '.join(v) if isinstance(v, list) else v}")
                processed = processed.replace(placeholder, "\n".join(dict_content))
            else:
                processed = processed.replace(placeholder, str(value))

        return processed

    def _get_about_technical_template(self) -> str:
        """Generate technical-focused about section template."""
        return """# {{title}} | Cloud Architecture & Performance Expert

## Technical Expertise

{{tech_stack}}

## Core Competencies

### Frontend Development
- **React Ecosystem**: Advanced React patterns, performance optimization, state management
- **Modern JavaScript**: ES2022+, TypeScript, WebAssembly integration
- **CSS Architecture**: Tailwind CSS, CSS-in-JS, design systems, responsive design
- **Performance**: Core Web Vitals optimization, code splitting, lazy loading strategies

### Backend & Architecture
- **API Design**: RESTful APIs, GraphQL, real-time communication (WebSockets)
- **Database Systems**: PostgreSQL optimization, MongoDB design, Redis caching strategies
- **Cloud Architecture**: AWS services, serverless computing, microservices patterns
- **DevOps & CI/CD**: Docker, Kubernetes, GitHub Actions, infrastructure as code

### Specialized Skills
- **Real-Time Systems**: WebSocket implementations, live collaboration features
- **Performance Optimization**: Database query optimization, caching strategies
- **Security**: Authentication/authorization, encryption, security best practices
- **Scalability**: Load balancing, horizontal scaling, performance monitoring

## Technical Achievements

### High-Impact Projects
- **Scaled application**: From 1K to 100K daily users (100× growth)
- **Performance optimization**: 60% improvement in page load times
- **Cost reduction**: 40% decrease in cloud infrastructure costs
- **Team leadership**: Mentored {{team_size}} developers, established best practices

### Open Source Contributions
- **Maintainer**: {{open_source_projects}} popular packages
- **Community**: Active contributor to React and Node.js ecosystems
- **Speaking**: Tech talks on performance, architecture, and best practices

## Development Philosophy

### Code Quality
- **Clean Code**: SOLID principles, comprehensive testing, clear documentation
- **Performance-First**: Every decision considers performance implications
- **Scalable Architecture**: Design for growth from day one
- **Continuous Improvement**: Regular refactoring, dependency updates, security patches

### Problem-Solving Approach
1. **Understand Requirements**: Deep business context before technical solutions
2. **Architecture First**: Plan for scalability and maintainability
3. **Iterative Development**: Build incrementally with continuous feedback
4. **Measure Everything**: Performance metrics, user feedback, business impact

## Let's Connect

Interested in complex technical challenges or opportunities to build scalable systems? I'm always excited to discuss projects that push the boundaries of web technology.

**📧 Email**: {{email}}
**💼 LinkedIn**: {{linkedin}}
**🐙 GitHub**: {{github}}
**🌐 Portfolio**: {{portfolio}}

---

*"Building the future of web applications with clean, scalable, and performant code."*

### Current Availability
- **Open to opportunities**: {{availability}}
- **Preferred roles**: Senior/Lead positions, technical leadership
- **Technologies**: React/Node.js ecosystem, cloud architecture
- **Industries**: SaaS, e-commerce, fintech, real-time applications"""

    def _get_about_business_template(self) -> str:
        """Generate business-focused about section template."""
        return """# Strategic Technology Leader | Digital Transformation Expert

## Executive Summary

Results-oriented technology leader with {{years_experience}} years of experience driving digital transformation and building high-performing engineering teams. Proven track record of scaling technology platforms from startup to enterprise level while maintaining focus on business outcomes and user experience.

## Business Impact & Achievements

### Revenue Growth & Market Expansion
- **Revenue Impact**: Generated ${{revenue_impact}}M through technology-driven initiatives
- **Market Expansion**: Enabled entry into {{new_markets}} new markets
- **User Growth**: Accelerated user acquisition to {{user_growth}}M+ active users
- **Cost Optimization**: Reduced operational costs by {{cost_reduction}}% through strategic technology decisions

### Team Leadership & Organizational Development
- **Team Building**: Grew engineering teams from {{initial_team_size}} to {{final_team_size}} members
- **Talent Development**: Mentored {{mentored_developers}} developers who advanced to senior roles
- **Process Improvement**: Implemented development methodologies that increased delivery velocity by {{velocity_improvement}}%
- **Culture Building**: Established engineering culture focused on innovation and accountability

### Strategic Technology Initiatives
- **Digital Transformation**: Led company-wide technology modernization
- **Platform Migration**: Successfully migrated legacy systems to modern architecture
- **Product Innovation**: Launched {{new_products}} new products driving {{product_revenue}}% of revenue
- **Partnership Integration**: Established technology partnerships with {{key_partners}}

## Leadership Philosophy

### Strategic Vision
- **Business-First Technology**: Every technical decision tied to business outcomes
- **Customer-Centric Approach**: Deep understanding of user needs and market demands
- **Data-Driven Decisions**: Comprehensive analytics and performance measurement
- **Long-Term Thinking**: Sustainable technology investments and roadmaps

### Team Building & Management
- **Hiring Excellence**: Rigorous selection process focusing on both technical and cultural fit
- **Continuous Learning**: Investment in team development and skills enhancement
- **Performance Culture**: Clear expectations, regular feedback, and merit-based recognition
- **Cross-Functional Collaboration**: Strong partnerships with product, design, and business teams

## Industry Expertise

### Sectors & Domains
{{industry_expertise}}

### Technology Stack & Architecture
- **Leadership Experience**: Full-stack development, cloud architecture, DevOps
- **Scalability**: Systems supporting millions of users and billions of transactions
- **Security**: Enterprise-grade security implementations and compliance
- **Innovation**: AI/ML integration, real-time systems, emerging technologies

## Speaking & Thought Leadership

### Presentations & Conferences
- **Keynote Speaker**: {{keynote_count}}+ industry conferences
- **Panel Discussions**: Technology leadership, digital transformation topics
- **Workshop Facilitator**: Engineering leadership, agile methodologies
- **Guest Lecturer**: Technology entrepreneurship, software architecture

### Publications & Recognition
- **Industry Recognition**: {{industry_awards}} awards for technology innovation
- **Published Articles**: {{published_articles}}+ articles on technology and business strategy
- **Patent Holder**: {{patent_count}} patents in software architecture and systems design
- **Industry Advisory**: Technology advisor for {{advisory_roles}} startups

## Education & Certifications

### Academic Background
- **Education**: {{education}}
- **Continuous Learning**: Executive education in business leadership and strategy
- **Professional Certifications**: {{certifications}}

## Strategic Partnerships & Network

### Industry Connections
- **Board Memberships**: Technology advisory boards and industry associations
- **Investor Relations**: Connections with venture capital and private equity
- **Startup Ecosystem**: Mentor for technology accelerators and incubators
- **Global Network**: Professional relationships across multiple industries and geographies

## Current Focus & Future Vision

### 2024 Strategic Priorities
- **AI Integration**: Leveraging artificial intelligence for business optimization
- **Sustainability**: Green technology initiatives and carbon footprint reduction
- **Remote Work**: Building and leading distributed engineering teams
- **Digital Innovation**: Exploring emerging technologies for competitive advantage

### Long-Term Vision
Creating technology solutions that not only solve business problems but also contribute to positive social and environmental impact. Believing in responsible innovation that balances growth with sustainability.

## Let's Connect

I'm passionate about tackling complex business challenges through innovative technology solutions. Whether you're seeking strategic technology leadership, digital transformation expertise, or partnership opportunities, I'd welcome the conversation.

**📧 Email**: {{email}}
**💼 LinkedIn**: {{linkedin}}
**🌐 Company Website**: {{company_website}}
**📱 Phone**: {{phone}}

---

*"Transforming businesses through strategic technology leadership and innovation."*

### Executive Summary
- **Years Experience**: {{years_experience}}
- **Team Leadership**: Up to {{max_team_size}} engineers
- **Industry Expertise**: {{industry_count}}+ sectors
- **Geographic Reach**: {{geographic_reach}} countries
- **Languages**: {{languages}}"""

    def _get_about_casual_template(self) -> str:
        """Generate casual/friendly about section template."""
        return """# Hey, I'm {{name}}! 👋

I build cool things on the web and help teams create amazing digital experiences. When I'm not coding, you'll probably find me {{hobbies}}.

## What I Do

By day, I'm a **{{title}}** who loves turning complex problems into simple, beautiful solutions. By night, I'm usually {{night_activities}}.

### My Tech Toolbox

{{tech_stack}}

### Some Projects I'm Proud Of

{{featured_projects}}

### Things I Believe In
- **Code should be readable** - Future you will thank present you
- **Users come first** - Technology serves people, not the other way around
- **Continuous learning** - The web changes fast, and that's exciting!
- **Good coffee** - Essential for debugging sessions

## My Journey

Started coding {{started_coding}} and haven't stopped since. I've been lucky enough to work with amazing teams at places like {{previous_companies}}, where I got to build {{notable_projects}}.

These days, I'm particularly excited about:
- {{current_interest_1}}
- {{current_interest_2}}
- {{current_interest_3}}

## When I'm Not Coding

- **🎵 {{music_interests}}**
- **🏃 {{fitness_activities}}**
- **📚 {{reading_interests}}**
- **🌍 {{travel_interests}}**

## Let's Connect!

I'm always up for chatting about:
- Interesting tech projects
- Startup ideas
- {{other_interests}}
- Good coffee recommendations

**📧 Drop me a line**: {{email}}
**💼 LinkedIn**: {{linkedin}}
**🐙 GitHub**: {{github}}
**🐦 Twitter**: {{twitter}}

---

*"Life's too short for bad code and boring projects."* 🚀

### Fun Facts
- **First program**: A {{first_program}} that {{first_program_result}}
- **Proudest moment**: {{proudest_moment}}
- **Superpower**: {{superpower}}
- **Dream project**: {{dream_project}}

### Current Status
- **Looking for**: {{looking_for}}
- **Available for**: {{available_for}}
- **Location**: {{location}}
- **Time zone**: {{timezone}}"""

    def _get_about_leadership_template(self) -> str:
        """Generate leadership-focused about section template."""
        return """# Technology Leader & Team Builder | Scaling Engineering Organizations

## Executive Summary

Experienced technology leader with {{years_experience}} years of experience building and scaling high-performing engineering organizations. Proven track record of delivering complex technology initiatives while fostering innovation, mentorship, and operational excellence.

## Leadership Experience

### Engineering Leadership
- **Team Scale**: Led teams from {{initial_team_size}} to {{final_team_size}}+ engineers
- **Geographic Distribution**: Managed distributed teams across {{countries}}+ countries
- **Budget Responsibility**: Oversaw technology budgets of ${{budget_range}}M
- **Reporting Structure**: Reported to CTO/CEO and managed {{direct_reports}} direct reports

### Strategic Impact
- **Platform Architecture**: Designed and implemented scalable systems supporting {{user_scale}}M+ users
- **Digital Transformation**: Led company-wide technology modernization initiatives
- **Product Innovation**: Drove development of {{new_products}} products generating ${{product_revenue}}M+ revenue
- **Operational Excellence**: Improved engineering velocity by {{velocity_improvement}}% through process optimization

### Organizational Development

#### Team Building & Culture
- **Hiring Excellence**: Built world-class engineering teams with {{hiring_success_rate}}% retention
- **Talent Development**: Promoted {{promotions_count}} engineers to senior/staff positions
- **Mentorship Programs**: Established formal mentorship benefiting {{mentored_count}}+ engineers
- **Inclusive Culture**: Increased diversity in engineering teams by {{diversity_improvement}}%

#### Process & Operations
- **Agile Transformation**: Implemented SAFe/Scrum methodologies across {{teams_count}} teams
- **DevOps Implementation**: Established CI/CD pipelines reducing deployment time by {{deployment_improvement}}%
- **Quality Engineering**: Built comprehensive testing strategy achieving {{test_coverage}}% coverage
- **Technology Governance**: Established architecture review processes and standards

## Technical Strategy & Vision

### Architecture Leadership
- **Microservices Adoption**: Led migration from monolith to microservices architecture
- **Cloud Strategy**: Executed cloud migration achieving {{cloud_migration_savings}}% cost savings
- **Data Strategy**: Implemented real-time analytics and machine learning capabilities
- **Security**: Established enterprise-grade security and compliance frameworks

### Innovation & R&D
- **Technology Radar**: Evaluated and adopted emerging technologies
- **Proof of Concepts**: Led innovation labs exploring AI/ML, blockchain, and IoT applications
- **Patents**: Filed {{patent_count}} patents for novel technical solutions
- **Open Source**: Contributed to {{open_source_projects}} open source projects

## Business Acumen & Partnerships

### Stakeholder Management
- **Executive Communication**: Regular presentations to board and C-level executives
- **Cross-Functional Leadership**: Strong partnerships with Product, Design, Marketing, and Sales
- **Customer Relations**: Direct engagement with enterprise clients and strategic partners
- **Vendor Management**: Negotiated contracts with technology vendors and service providers

### Financial Impact
- **Budget Optimization**: Reduced technology spend by {{budget_optimization}}% while improving capabilities
- **ROI Focus**: Delivered {{roi_percentage}}% average ROI on technology investments
- **Cost Management**: Implemented FinOps practices optimizing cloud spend
- **Revenue Enablement**: Technology initiatives directly contributed to {{revenue_contribution}}% revenue growth

## Industry Recognition & Thought Leadership

### Speaking & Conferences
- **Keynote Speaker**: {{keynote_count}}+ major technology conferences
- **Panelist**: {{panel_count}} industry panels on technology leadership
- **Workshop Leader**: Conducted {{workshop_count}}+ engineering leadership workshops
- **Guest Lecturer**: {{lectures_count}}+ university lectures on software engineering

### Publications & Media
- **Articles**: Published {{articles_count}}+ articles on technology and leadership
- **Books**: Authored/co-authored {{book_count}} books on software engineering
- **Podcasts**: Featured on {{podcast_count}}+ technology podcasts
- **Awards**: Recipient of {{award_count}}+ industry recognitions

## Education & Professional Development

### Academic Background
{{education}}

### Executive Education
- **Leadership Programs**: {{leadership_programs}}
- **Business Strategy**: {{business_programs}}
- **Technology Management**: {{tech_management_programs}}

### Certifications & Associations
- **Professional Certifications**: {{certifications}}
- **Industry Associations**: {{professional_associations}}
- **Board Positions**: {{board_positions}}

## Current Role & Responsibilities

As {{current_role}} at {{current_company}}, I'm responsible for:

### Strategic Leadership
- **Technology Vision**: Define and execute technology strategy aligned with business objectives
- **Team Leadership**: Build, mentor, and scale world-class engineering organizations
- **Innovation**: Drive technology innovation and competitive differentiation
- **Operational Excellence**: Ensure high-quality, reliable, and scalable technology operations

### Key Initiatives
{{current_initiatives}}

## Mentorship & Community Involvement

### Mentoring
- **Internal Mentoring**: {{internal_mentees}} engineers currently in formal mentorship
- **External Advisory**: Technology advisor for {{advised_companies}} startups
- **Startup Ecosystem**: Mentor at {{accelerators}} technology accelerators
- **Industry Education**: Regular speaker at industry events and universities

### Community Leadership
- **Open Source**: Maintainer and contributor to {{oss_projects}} open source projects
- **Technology Meetups**: Organizer/speaker at local technology communities
- **Diversity & Inclusion**: Advocate for diversity in technology and STEM education
- **Non-Profit**: Technology advisor for {{non_profits}} non-profit organizations

## Future Vision & Interests

### Technology Trends
- **Artificial Intelligence**: Practical applications and ethical considerations
- **Distributed Systems**: Edge computing and decentralized architectures
- **Sustainability**: Green technology and carbon-efficient computing
- **Remote Work**: Future of distributed engineering organizations

### Personal Growth
- **Continuous Learning**: Executive education in business and technology trends
- **Global Perspective**: International technology markets and cultural diversity
- **Social Impact**: Using technology for positive social and environmental impact
- **Knowledge Sharing**: Mentoring the next generation of technology leaders

## Let's Connect

I'm passionate about building great technology, leading high-performing teams, and creating positive business impact. I'm always interested in connecting with fellow technology leaders, innovators, and organizations working on challenging problems.

**📧 Email**: {{email}}
**💼 LinkedIn**: {{linkedin}}
**🌐 Company**: {{company_website}}
**📱 Phone**: {{phone}}
**📍 Location**: {{location}}

---

*"Building technology organizations that innovate at scale while nurturing human potential."*

### Leadership Philosophy
- **People First**: Technology is built by people, for people
- **Vision with Execution**: Bold thinking paired with pragmatic implementation
- **Continuous Learning**: Embrace change and foster growth mindset
- **Inclusive Excellence**: Diversity drives innovation and better outcomes"""

    def _get_job_application_template(self) -> str:
        """Generate job application email template."""
        return """Subject: Application for {{position}} - {{name}}

Dear {{hiring_manager}},

I'm writing to express my strong interest in the {{position}} position at {{company_name}}. With {{years_experience}} years of experience in full-stack development and a proven track record of building scalable applications, I'm excited about the opportunity to contribute to your team.

## Why {{company_name}}?

I've been following {{company_name}}'s work in the {{industry}} space and am particularly impressed by:
- {{company_achievement_1}}
- {{company_achievement_2}}
- Your commitment to {{company_value}}

Your focus on {{specific_focus}} aligns perfectly with my experience and passion for building products that make a real impact.

## My Relevant Experience

### Technical Expertise
- **Frontend**: {{frontend_expertise}}
- **Backend**: {{backend_expertise}}
- **Cloud & DevOps**: {{devops_expertise}}
- **Database**: {{database_expertise}}

### Key Achievements
- **Project Success**: Built {{notable_project}} that achieved {{project_result}}
- **Performance Impact**: Improved {{metric}} by {{improvement_percentage}}%
- **Team Leadership**: Led team of {{team_size}} developers on {{initiative}}
- **Business Value**: Generated {{business_impact}} through technical solutions

### Why I'm a Great Fit
1. **{{skill_1}}**: {{skill_1_detail}}
2. **{{skill_2}}**: {{skill_2_detail}}
3. **{{skill_3}}**: {{skill_3_detail}}

## Understanding Your Needs

Based on the job description and my research, I understand you're looking for someone who can:

{{job_requirements}}

My experience with {{relevant_experience}} has prepared me well to meet these challenges and contribute immediately to your team.

## Portfolio Highlights

Here are a few projects that demonstrate my capabilities:

{{portfolio_projects}}

## Next Steps

I would love the opportunity to discuss how my experience with {{key_technology}} and my approach to {{development_philosophy}} can help {{company_name}} achieve {{company_goal}}.

Are you available for a {{interview_length}} call next week? I'm flexible on timing and eager to learn more about this opportunity.

Thank you for considering my application. I look forward to hearing from you.

Best regards,

{{name}}
{{email}} | {{phone}}
{{portfolio}} | {{linkedin}} | {{github}}

---
Attachments:
- Resume
- Portfolio link: {{portfolio}}
- Code samples: {{github_samples}}
"""

    def _get_freelance_proposal_template(self) -> str:
        """Generate freelance project proposal template."""
        return """Subject: Proposal for {{project_type}} Development - {{name}}

Hi {{client_name}},

Thank you for reaching out about your {{project_type}} project. Based on our discussion and your requirements, I'm excited to submit this proposal for developing {{project_overview}}.

## Project Understanding

You're looking to build a {{project_description}} that will:

{{project_goals}}

The main challenges you're facing include:
- {{challenge_1}}
- {{challenge_2}}
- {{challenge_3}}

## Proposed Solution

I recommend building a {{solution_architecture}} that will:

### Core Features
{{core_features}}

### Technical Approach
- **Frontend**: {{frontend_solution}}
- **Backend**: {{backend_solution}}
- **Database**: {{database_solution}}
- **Deployment**: {{deployment_solution}}

### Why This Approach
- **Scalability**: Designed to handle {{expected_users}} users
- **Performance**: Optimized for {{performance_requirements}}
- **Maintainability**: Clean code with comprehensive testing
- **Security**: Enterprise-grade security measures

## Project Timeline

{{project_timeline}}

## Investment

**Total Project Cost**: ${{total_cost}}

**Payment Schedule**:
- {{payment_schedule}}

This includes:
- ✅ Full development and testing
- ✅ Deployment and setup
- ✅ {{support_period}} days of post-launch support
- ✅ Documentation and knowledge transfer

## Why Choose Me

### Relevant Experience
- **Similar Projects**: Built {{similar_project_count}}+ similar applications
- **Technical Expertise**: {{years_experience}} years in {{relevant_tech}}
- **Business Understanding**: Experience with {{industry_knowledge}}
- **Proven Results**: {{success_metrics}}

### Development Process
1. **Discovery Phase**: Deep dive into requirements and user needs
2. **Design Phase**: Wireframes, mockups, and technical architecture
3. **Development**: Iterative development with regular check-ins
4. **Testing**: Comprehensive testing including user acceptance
5. **Deployment**: Smooth launch with monitoring setup
6. **Support**: Post-launch optimization and maintenance

### Client Testimonials
{{client_testimonials}}

## Next Steps

If this proposal looks good, here's what happens next:

1. **Approval**: Sign this proposal and pay {{initial_payment}} deposit
2. **Kickoff**: Schedule project kickoff meeting
3. **Development**: Begin development with regular progress updates
4. **Delivery**: Launch your new application!

I'm available to start on {{start_date}} and estimate completion by {{completion_date}.

Do you have any questions or would you like to schedule a call to discuss further?

Looking forward to potentially working together!

Best regards,

{{name}}
{{email}} | {{phone}}
{{portfolio}} | {{linkedin}}

---
**Proposal Valid Until**: {{proposal_valid_date}}
**Revision Policy**: {{revision_policy}}
**Project Terms**: {{project_terms}}
"""

    def _get_networking_template(self) -> str:
        """Generate professional networking email template."""
        return """Subject: {{networking_purpose}} - {{name}}

Hi {{contact_name}},

{{opening_sentence}}

{{connection_reason}}

{{shared_interests}}

{{value_proposition}}

Would you be open to a brief {{meeting_length}} call in the coming weeks? I'd love to:

{{discussion_points}}

I know you're busy, so completely understand if your schedule doesn't allow right now. Either way, I'll continue following your work on {{where_to_follow}}.

Thank you for your time and consideration.

Best regards,

{{name}}
{{email}} | {{phone}}
{{portfolio}} | {{linkedin}}

P.S. {{postscript}}
"""

    def _get_follow_up_template(self) -> str:
        """Generate follow-up email template."""
        return """Subject: {{follow_up_subject}} - {{name}}

Hi {{contact_name}},

{{follow_up_context}}

{{key_points}}

{{next_step}}

{{call_to_action}}

Thank you for your time and consideration.

Best regards,

{{name}}
{{email}} | {{phone}}
{{portfolio}} | {{linkedin}}
"""

    def _get_thank_you_template(self) -> str:
        """Generate thank you email template."""
        return """Subject: Thank You - {{meeting_topic}}

Dear {{contact_name}},

Thank you so much for your time today discussing {{meeting_topic}}. I really enjoyed our conversation and appreciate you sharing your insights about {{specific_topic}}.

{{key_takeaways}}

{{excitement_about_future}}

{{next_steps}}

Please don't hesitate to reach out if {{offer_help}}.

Looking forward to potentially working together!

Best regards,

{{name}}
{{email}} | {{phone}}
{{portfolio}} | {{linkedin}}
"""

    def _get_project_technical_template(self) -> str:
        """Generate technical project summary template."""
        return """# {{project_name}} - Technical Overview

## Architecture Summary

{{architecture_overview}}

## Technology Stack

### Frontend
{{frontend_tech}}

### Backend
{{backend_tech}}

### Database
{{database_tech}}

### Infrastructure
{{infrastructure_tech}}

## Key Technical Decisions

{{technical_decisions}}

## Performance Metrics

{{performance_metrics}}

## Scalability Features

{{scalability_features}}

## Security Implementation

{{security_features}}

## Code Quality

{{code_quality_metrics}}

## Deployment & DevOps

{{deployment_process}}
"""

    def _get_project_business_template(self) -> str:
        """Generate business-focused project summary template."""
        return """# {{project_name}} - Business Impact Summary

## Executive Summary

{{executive_summary}}

## Business Problem Solved

{{business_problem}}

## Solution Overview

{{solution_overview}}

## Key Features & Benefits

{{features_and_benefits}}

## Measurable Results

{{business_results}}

## User Impact

{{user_impact}}

## Market Position

{{market_position}}

## Competitive Advantages

{{competitive_advantages}}

## ROI & Financial Impact

{{financial_impact}}

## Future Growth Potential

{{growth_potential}}

## Lessons Learned

{{business_lessons}}
"""

    def _get_project_demo_template(self) -> str:
        """Generate demo-focused project summary template."""
        return """# {{project_name}} - Live Demo

## Quick Overview

{{demo_overview}}

## What This Demo Shows

{{demo_highlights}}

## How to Use

{{demo_instructions}}

## Key Features to Try

{{demo_features}}

## Technical Stack

{{demo_tech_stack}}

## Performance Highlights

{{performance_highlights}}

## Behind the Scenes

{{behind_scenes}}

## Try It Yourself

**Live Demo**: {{demo_url}}
**Source Code**: {{github_url}}
**Documentation**: {{docs_url}}

## Questions?

{{demo_support}}
"""

    def _get_linkedin_template(self) -> str:
        """Generate LinkedIn post template."""
        return """{{hook}}

{{main_content}}

{{key_achievements}}

{{lessons_learned}}

{{call_to_action}}

{{hashtags}}

#{{primary_hashtag}}
"""

    def _get_twitter_template(self) -> str:
        """Generate Twitter post template."""
        return """{{twitter_hook}}

{{twitter_content}}

{{twitter_cta}}

{{twitter_hashtags}}
"""

    def _get_github_template(self) -> str:
        """Generate GitHub README template."""
        return """# {{project_name}}

{{project_description}}

## 🚀 Features

{{features}}

## 🛠️ Tech Stack

{{tech_stack}}

## 📦 Installation

{{installation}}

## 🏃‍♂️ Usage

{{usage}}

## 🧪 Testing

{{testing}}

## 📈 Performance

{{performance}}

## 🤝 Contributing

{{contributing}}

## 📄 License

{{license}}

## 👨‍💻 Author

{{author_info}}

## 🙏 Acknowledgments

{{acknowledgments}}
"""

    def create_template(self, name: str, fields: List[str]) -> str:
        """Create a new custom template."""
        template_content = f"""
# Custom Template: {name}

## Template Fields
{chr(10).join(f"- {{{{{field}}}}}" for field in fields)}

## Usage Instructions
This template can be customized by providing values for the fields above.

## Example Usage
```python
from template_engine import PortfolioTemplateEngine

engine = PortfolioTemplateEngine()
content = engine.generate('custom', name, **{{
    'field1': 'value1',
    'field2': 'value2'
}})
```
"""
        return template_content.strip()


def main():
    parser = argparse.ArgumentParser(description="Generate portfolio content using templates")
    parser.add_argument("command", choices=["generate", "create-template", "list-templates"],
                       help="Command to execute")
    parser.add_argument("--template", required=True, help="Template name")
    parser.add_argument("--style", help="Template style/variant")
    parser.add_argument("--name", help="Template name for create-template")
    parser.add_argument("--fields", help="Comma-separated fields for create-template")
    parser.add_argument("--tech-stack", help="Path to tech stack JSON file")
    parser.add_argument("--experience", help="Path to experience JSON file")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--purpose", help="Purpose of email template")
    parser.add_argument("--company", help="Company name for templates")
    parser.add_argument("--position", help="Position for job application")
    parser.add_argument("--hiring-manager", help="Hiring manager name")
    parser.add_argument("--contact-name", help="Contact name for networking")

    args = parser.parse_args()

    engine = PortfolioTemplateEngine()

    if args.command == "list-templates":
        print("Available templates:")
        for template_type, variants in engine.templates.items():
            print(f"  {template_type}: {', '.join(variants.keys())}")

    elif args.command == "create-template":
        if not args.name or not args.fields:
            print("Error: --name and --fields required for create-template")
            return

        fields = [field.strip() for field in args.fields.split(",")]
        template = engine.create_template(args.name, fields)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(template)

        print(f"✅ Template created: {output_path}")

    elif args.command == "generate":
        # Load additional data if provided
        context = {}

        if args.tech_stack:
            with open(args.tech_stack) as f:
                context['tech_stack'] = json.load(f)

        if args.experience:
            with open(args.experience) as f:
                context.update(json.load(f))

        # Add command-specific context
        if args.purpose:
            context['purpose'] = args.purpose
        if args.company:
            context['company_name'] = args.company
        if args.position:
            context['position'] = args.position
        if args.hiring_manager:
            context['hiring_manager'] = args.hiring_manager
        if getattr(args, 'contact_name', None):
            context['contact_name'] = getattr(args, 'contact_name')

        try:
            content = engine.generate(args.template, args.style, **context)

            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                f.write(content)

            print(f"✅ Content generated: {output_path}")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()