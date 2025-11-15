#!/usr/bin/env python3
"""
Example usage of the SEO Auditor for Developer Portfolios
Demonstrates how to analyze a developer portfolio and generate SEO recommendations
"""

import sys
import os
import json
from pathlib import Path

# Add the scripts directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from seo_auditor import SEOAuditor, SEOAuditResult
from keyword_researcher import KeywordResearcher
from meta_generator import MetaTagGenerator
from schema_generator import SchemaGenerator


def example_seo_audit():
    """Example: Complete SEO audit of a developer portfolio"""

    print("🔍 SEO AUDIT EXAMPLE - Developer Portfolio")
    print("=" * 60)

    # Sample portfolio HTML content
    portfolio_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>John Doe - Developer</title>
        <meta name="description" content="My portfolio projects">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <h1>John Doe</h1>
        <h2>About Me</h2>
        <p>I am a software developer with experience in React and Node.js.</p>
        <h3>Projects</h3>
        <img src="project1.jpg" alt="Project screenshot">
        <img src="project2.jpg"> <!-- Missing alt text -->

        <section>
            <h2>Skills</h2>
            <p>Experienced in React, Node.js, TypeScript, and Python.</p>
        </section>

        <section>
            <h2>Contact</h2>
            <p>Email me at john@example.com for opportunities.</p>
        </section>
    </body>
    </html>
    """

    # Initialize the SEO auditor
    auditor = SEOAuditor()

    # Perform the audit
    print("\n📊 Running SEO Audit...")
    result = auditor.audit_portfolio("https://johndoe.dev", portfolio_html)

    # Generate and display the audit report
    report = auditor.generate_audit_report(result)
    print("\n" + report)

    return result


def example_keyword_research():
    """Example: Keyword research for a developer portfolio"""

    print("\n🔍 KEYWORD RESEARCH EXAMPLE")
    print("=" * 40)

    # Sample portfolio content
    portfolio_content = """
    John Doe - Senior React Developer

    I am a senior software developer with 8 years of experience building
    web applications using React, Node.js, and TypeScript. I have worked
    on e-commerce platforms and financial technology applications.

    Currently located in San Francisco and available for remote opportunities.

    Technologies: React, Node.js, TypeScript, Python, AWS, Docker
    """

    # Initialize keyword researcher
    researcher = KeywordResearcher()

    # Perform keyword research
    print("\n📈 Performing Keyword Research...")
    research_results = researcher.research_keywords(
        content=portfolio_content,
        location="San Francisco",
        technologies=["React", "Node.js", "TypeScript", "Python"]
    )

    # Display results
    print(f"\n🎯 Found {sum(len(keywords) for keywords in research_results['existing_keywords'].values())} existing keywords")

    # Display top opportunities
    print("\n🚀 Top Keyword Opportunities:")
    for i, opportunity in enumerate(research_results['opportunities'][:3], 1):
        print(f"{i}. {opportunity['keyword']}")
        print(f"   Priority: {opportunity['priority']}")
        print(f"   Estimated Traffic: {opportunity['estimated_traffic']}/month")
        print(f"   Action: {opportunity['action']}")

    return research_results


def example_meta_generation():
    """Example: Generate optimized meta tags"""

    print("\n📝 META TAG GENERATION EXAMPLE")
    print("=" * 40)

    # Sample portfolio data
    portfolio_data = {
        "name": "Sarah Chen",
        "title": "Senior React Developer",
        "location": "San Francisco, CA",
        "technologies": ["React", "Node.js", "TypeScript", "Python"],
        "experience_level": "Senior",
        "bio": "Experienced React developer with 8+ years building scalable web applications for fintech startups.",
        "url": "https://sarahchen.dev",
        "image_url": "https://sarahchen.dev/images/profile.jpg",
        "github": "sarahchen",
        "linkedin": "sarahchen",
        "twitter": "sarahchen_dev",
        "years_experience": "8+",
        "work_type": "full-time and contract opportunities",
        "achievements": "Led development of trading platform handling $50M+ daily volume",
        "email": "sarah@sarahchen.dev"
    }

    # Initialize meta tag generator
    generator = MetaTagGenerator()

    # Generate meta tags
    print("\n🔧 Generating Optimized Meta Tags...")
    meta_tags = generator.generate_meta_tags(portfolio_data)

    # Display generated title and description
    print(f"\n✅ Generated Title: {meta_tags.title}")
    print(f"✅ Generated Description: {meta_tags.description}")
    print(f"✅ Keywords: {meta_tags.keywords[:100]}...")

    # Display optimization score
    score_data = generator._calculate_optimization_score(meta_tags)
    print(f"\n📊 SEO Optimization Score: {score_data['percentage']}%")

    print("\n📋 Optimization Feedback:")
    for feedback in score_data['feedback']:
        print(f"   {feedback}")

    return meta_tags


def example_schema_generation():
    """Example: Generate structured data for a developer portfolio"""

    print("\n🏗️  SCHEMA GENERATION EXAMPLE")
    print("=" * 40)

    # Sample portfolio data
    portfolio_data = {
        "name": "Sarah Chen",
        "title": "Senior React Developer",
        "description": "Senior React Developer with 8+ years building scalable web applications for fintech startups.",
        "bio": "Experienced React developer with 8+ years building scalable web applications for fintech startups.",
        "url": "https://sarahchen.dev",
        "image_url": "https://sarahchen.dev/images/profile.jpg",
        "email": "sarah@sarahchen.dev",
        "phone": "+1-555-0123",
        "location": "San Francisco, CA",
        "github": "sarahchen",
        "linkedin": "sarahchen",
        "twitter": "sarahchen_dev",
        "technologies": ["React", "Node.js", "TypeScript", "Python", "AWS"],
        "available_for_hire": True,
        "job_types": ["FULL_TIME", "CONTRACTOR"],
        "projects": [
            {
                "name": "Algorithmic Trading Platform",
                "description": "Real-time trading platform for hedge funds",
                "url": "https://sarahchen.dev/projects/trading-platform",
                "repository_url": "https://github.com/sarahchen/trading-platform",
                "technologies": ["React", "Node.js", "TypeScript", "WebSocket"],
                "start_date": "2023-01",
                "status": "completed",
                "role": "Lead Developer"
            }
        ],
        "work_experience": [
            {
                "company": "TechVenture Capital",
                "position": "Senior React Developer",
                "start_date": "2021-01",
                "current_job": True,
                "location": "San Francisco, CA",
                "technologies": ["React", "TypeScript", "Node.js"],
                "achievements": ["Led development of trading platform", "Improved performance by 60%"]
            }
        ],
        "education": [
            {
                "institution": "Stanford University",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2015-09",
                "end_date": "2019-05"
            }
        ]
    }

    # Initialize schema generator
    generator = SchemaGenerator()

    # Generate structured data
    print("\n🔧 Generating Structured Data...")
    structured_data = generator.generate_complete_schema(portfolio_data)

    # Validate schema
    validation = generator.validate_schema(structured_data)
    print(f"\n✅ Schema Validation: {'Passed' if validation['valid'] else 'Failed'}")

    if validation['suggestions']:
        print("\n💡 Schema Optimization Suggestions:")
        for suggestion in validation['suggestions']:
            print(f"   • {suggestion}")

    # Display schema statistics
    if isinstance(structured_data, dict) and '@graph' in structured_data:
        print(f"\n📊 Generated {len(structured_data['@graph'])} schema types:")
        for schema in structured_data['@graph']:
            schema_type = schema.get('@type', 'Unknown')
            if isinstance(schema_type, list):
                schema_type = ', '.join(schema_type)
            print(f"   • {schema_type}")

    return structured_data


def example_portfolio_optimization_report():
    """Example: Generate comprehensive portfolio optimization report"""

    print("\n📋 COMPREHENSIVE OPTIMIZATION REPORT")
    print("=" * 50)

    # Run all analyses
    print("Running complete portfolio analysis...\n")

    # 1. SEO Audit
    audit_result = example_seo_audit()

    # 2. Keyword Research
    keyword_results = example_keyword_research()

    # 3. Meta Tag Generation
    meta_tags = example_meta_generation()

    # 4. Schema Generation
    schema_data = example_schema_generation()

    # Generate comprehensive report
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE PORTFOLIO OPTIMIZATION REPORT")
    print("=" * 60)

    # Overall score calculation
    seo_score = audit_result.score
    keyword_opportunities = len(keyword_results['opportunities'])
    meta_optimization = meta_tags and True  # Meta tags generated successfully
    schema_validation = True  # Assume schema is valid for this example

    overall_score = (seo_score + (keyword_opportunities * 5)) / 2
    overall_score = min(100, overall_score)  # Cap at 100

    print(f"\n🎯 OVERALL SEO SCORE: {overall_score:.0f}/100")

    # Grade assignment
    if overall_score >= 90:
        grade = "A+ (Excellent)"
    elif overall_score >= 80:
        grade = "A (Very Good)"
    elif overall_score >= 70:
        grade = "B (Good)"
    elif overall_score >= 60:
        grade = "C (Fair)"
    else:
        grade = "D (Needs Improvement)"

    print(f"Grade: {grade}")

    # Key metrics
    print(f"\n📈 KEY METRICS:")
    print(f"• Technical SEO Score: {seo_score}/100")
    print(f"• Keyword Opportunities: {keyword_opportunities}")
    print(f"• Meta Tags Optimized: {'✅' if meta_optimization else '❌'}")
    print(f"• Schema Markup: {'✅' if schema_validation else '❌'}")

    # Priority recommendations
    print(f"\n🚀 PRIORITY OPTIMIZATIONS:")

    # Top 3 issues from audit
    critical_issues = [issue for issue in audit_result.issues if issue['type'] == 'critical'][:3]
    if critical_issues:
        print("\n🔥 Critical Issues to Fix:")
        for i, issue in enumerate(critical_issues, 1):
            print(f"{i}. {issue['message']}")
            print(f"   Impact: {issue['impact']}")

    # Top keyword opportunities
    top_keywords = keyword_results['opportunities'][:3]
    if top_keywords:
        print("\n🎯 Top Keyword Opportunities:")
        for i, keyword in enumerate(top_keywords, 1):
            print(f"{i}. {keyword['keyword']} ({keyword['estimated_traffic']}/month)")
            print(f"   Action: {keyword['action']}")

    # Content gaps
    content_gaps = keyword_results['content_gaps'][:3]
    if content_gaps:
        print("\n📝 Content Gaps to Address:")
        for i, gap in enumerate(content_gaps, 1):
            print(f"{i}. {gap}")

    # Technical improvements
    print("\n🔧 Technical Improvements:")
    print("1. Optimize title tag (50-60 characters with keywords)")
    print("2. Improve meta description (120-160 characters)")
    print("3. Add alt text to all images")
    print("4. Implement proper heading structure")
    print("5. Add location-specific keywords")

    # Next steps
    print("\n📋 NEXT STEPS:")
    print("1. Implement critical technical fixes first")
    print("2. Optimize meta tags and structured data")
    print("3. Add content addressing keyword gaps")
    print("4. Monitor performance in Google Search Console")
    print("5. Re-audit after implementing changes")

    print("\n✨ Your portfolio will be highly optimized for recruiter searches!")

    return {
        'audit_result': audit_result,
        'keyword_results': keyword_results,
        'meta_tags': meta_tags,
        'schema_data': schema_data,
        'overall_score': overall_score
    }


if __name__ == "__main__":
    print("🚀 SEO OPTIMIZER FOR DEVELOPER PORTFOLIOS - EXAMPLES")
    print("=" * 60)

    try:
        # Run the complete example
        comprehensive_report = example_portfolio_optimization_report()

        print("\n" + "=" * 60)
        print("✅ Analysis Complete! Your portfolio optimization report is ready.")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error running analysis: {e}")
        import traceback
        traceback.print_exc()