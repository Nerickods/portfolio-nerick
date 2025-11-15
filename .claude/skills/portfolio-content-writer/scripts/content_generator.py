#!/usr/bin/env python3
"""
Portfolio Content Generator

Main script for generating professional portfolio content including
project descriptions, about sections, blog posts, and contact templates.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class PortfolioContentGenerator:
    """Generate professional portfolio content from project data."""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.tech_stack = {}
        self.project_info = {}
        self.metrics = {}

    def analyze_project(self) -> Dict[str, Any]:
        """Analyze project structure and extract key information."""
        analysis = {
            "project_name": self._extract_project_name(),
            "tech_stack": self._extract_tech_stack(),
            "features": self._extract_features(),
            "commits": self._analyze_commits(),
            "metrics": self._estimate_metrics(),
            "files": self._analyze_files(),
            "dependencies": self._analyze_dependencies(),
        }
        return analysis

    def _extract_project_name(self) -> str:
        """Extract project name from package.json or directory name."""
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    return data.get("name", self.project_path.name)
            except:
                pass
        return self.project_path.name

    def _extract_tech_stack(self) -> Dict[str, List[str]]:
        """Extract technology stack from project files."""
        tech_stack = {
            "frontend": [],
            "backend": [],
            "database": [],
            "devops": [],
            "testing": [],
            "styling": []
        }

        # Analyze package.json
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

                    frontend_tech = ["react", "vue", "angular", "svelte", "next", "nuxt", "gatsby"]
                    backend_tech = ["express", "fastify", "django", "flask", "rails", "laravel", "spring"]
                    database_tech = ["mongodb", "postgresql", "mysql", "redis", "sqlite", "prisma", "typeorm"]
                    testing_tech = ["jest", "vitest", "cypress", "playwright", "pytest", "rspec"]
                    styling_tech = ["tailwind", "sass", "styled-components", "emotion", "material-ui"]

                    for dep in deps:
                        for tech in frontend_tech:
                            if tech in dep.lower():
                                tech_stack["frontend"].append(dep)
                        for tech in backend_tech:
                            if tech in dep.lower():
                                tech_stack["backend"].append(dep)
                        for tech in database_tech:
                            if tech in dep.lower():
                                tech_stack["database"].append(dep)
                        for tech in testing_tech:
                            if tech in dep.lower():
                                tech_stack["testing"].append(dep)
                        for tech in styling_tech:
                            if tech in dep.lower():
                                tech_stack["styling"].append(dep)
            except:
                pass

        # Analyze other files
        dockerfile = self.project_path / "Dockerfile"
        if dockerfile.exists():
            tech_stack["devops"].append("Docker")

        requirements_txt = self.project_path / "requirements.txt"
        if requirements_txt.exists():
            tech_stack["backend"].append("Python")

        gemfile = self.project_path / "Gemfile"
        if gemfile.exists():
            tech_stack["backend"].append("Ruby on Rails")

        return tech_stack

    def _extract_features(self) -> List[str]:
        """Extract features from README and source files."""
        features = []

        # Analyze README
        readme_files = ["README.md", "readme.md", "README.rst"]
        for readme_file in readme_files:
            readme_path = self.project_path / readme_file
            if readme_path.exists():
                try:
                    with open(readme_path) as f:
                        content = f.read()
                        # Look for feature lists
                        feature_patterns = [
                            r"## Features\n(.*?)(?=##|\n\n|$)",
                            r"### Features\n(.*?)(?=###|\n\n|$)",
                            r"\* (.*)",
                            r"- (.*)"
                        ]
                        for pattern in feature_patterns:
                            matches = re.findall(pattern, content, re.DOTALL)
                            for match in matches:
                                if len(match.strip()) > 10:
                                    features.append(match.strip())
                except:
                    pass

        # Analyze source files for comments
        for ext in [".js", ".jsx", ".ts", ".tsx", ".py", ".rb", ".php"]:
            for file_path in self.project_path.rglob(f"*{ext}"):
                if file_path.is_file() and not any(skip in str(file_path) for skip in ["node_modules", ".git", "dist"]):
                    try:
                        with open(file_path) as f:
                            lines = f.readlines()
                            for line in lines:
                                if "// TODO:" in line or "# TODO:" in line or "TODO:" in line:
                                    features.append(f"Implementation: {line.strip()}")
                                if "// FEATURE:" in line or "# FEATURE:" in line:
                                    features.append(f"Feature: {line.strip()}")
                    except:
                        pass

        return list(set(features[:10]))  # Limit to top 10 unique features

    def _analyze_commits(self) -> Dict[str, Any]:
        """Analyze git commit history for project insights."""
        commits = {
            "total_commits": 0,
            "recent_commits": [],
            "features_added": [],
            "bugs_fixed": [],
            "refactoring": []
        }

        try:
            import subprocess
            result = subprocess.run(
                ["git", "-C", str(self.project_path), "log", "--oneline", "-20"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                commit_lines = result.stdout.strip().split("\n")
                commits["total_commits"] = len(commit_lines)
                commits["recent_commits"] = commit_lines[:5]

                for commit in commit_lines:
                    commit_lower = commit.lower()
                    if any(word in commit_lower for word in ["feat", "add", "new"]):
                        commits["features_added"].append(commit)
                    elif any(word in commit_lower for word in ["fix", "bug", "resolve"]):
                        commits["bugs_fixed"].append(commit)
                    elif any(word in commit_lower for word in ["refactor", "clean", "improve"]):
                        commits["refactoring"].append(commit)
        except:
            pass

        return commits

    def _estimate_metrics(self) -> Dict[str, Any]:
        """Estimate project metrics and impact."""
        metrics = {
            "performance_improvements": [],
            "user_impact": [],
            "business_value": [],
            "technical_achievements": []
        }

        # File count as complexity metric
        file_count = len(list(self.project_path.rglob("*")))
        if file_count > 100:
            metrics["technical_achievements"].append(f"Complex project with {file_count}+ files")

        # Tech stack diversity
        tech_stack = self._extract_tech_stack()
        total_tech = sum(len(tech) for tech in tech_stack.values())
        if total_tech > 5:
            metrics["technical_achievements"].append(f"Diverse tech stack with {total_tech} technologies")

        # Estimate impact based on features
        features = self._extract_features()
        if len(features) > 5:
            metrics["user_impact"].append(f"Comprehensive solution with {len(features)}+ features")

        # Look for performance-related keywords
        performance_keywords = ["optimize", "performance", "speed", "cache", "efficient"]
        for feature in features:
            if any(keyword in feature.lower() for keyword in performance_keywords):
                metrics["performance_improvements"].append(feature)

        return metrics

    def _analyze_files(self) -> Dict[str, int]:
        """Analyze project file structure."""
        file_analysis = {
            "total_files": 0,
            "source_files": 0,
            "config_files": 0,
            "test_files": 0,
            "doc_files": 0
        }

        for file_path in self.project_path.rglob("*"):
            if file_path.is_file():
                file_analysis["total_files"] += 1

                suffix = file_path.suffix.lower()
                if suffix in [".js", ".jsx", ".ts", ".tsx", ".py", ".rb", ".php", ".java", ".cpp", ".c"]:
                    file_analysis["source_files"] += 1
                elif suffix in [".json", ".yaml", ".yml", ".toml", ".ini"]:
                    file_analysis["config_files"] += 1
                elif any(test_word in file_path.name.lower() for test_word in ["test", "spec"]):
                    file_analysis["test_files"] += 1
                elif suffix in [".md", ".rst", ".txt", ".doc", ".pdf"]:
                    file_analysis["doc_files"] += 1

        return file_analysis

    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies for insights."""
        deps_analysis = {
            "total_dependencies": 0,
            "external_libraries": [],
            "frameworks": [],
            "tools": []
        }

        # Analyze package.json
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                    deps_analysis["total_dependencies"] = len(deps)

                    # Categorize dependencies
                    for dep, version in deps.items():
                        if any(framework in dep.lower() for framework in ["react", "vue", "angular", "express", "fastify"]):
                            deps_analysis["frameworks"].append(f"{dep}@{version}")
                        elif any(tool in dep.lower() for tool in ["webpack", "babel", "eslint", "jest", "tailwind"]):
                            deps_analysis["tools"].append(f"{dep}@{version}")
                        else:
                            deps_analysis["external_libraries"].append(f"{dep}@{version}")
            except:
                pass

        return deps_analysis

    def generate_project_description(self, analysis: Dict[str, Any]) -> str:
        """Generate a professional project description."""
        template = f"""
# {analysis['project_name'].replace('-', ' ').title()}

## 🎯 The Challenge
[Business problem and market context would go here]
*Consider: What problem does this solve? Who has this problem? Why is it important?*

## 💡 Solution Overview
[Brief technical approach simplified for business audience]
*Consider: High-level architecture, key technologies, unique approach*

## 🚀 Key Features & Impact

"""

        # Add features with impact statements
        features = analysis['features'][:5]  # Top 5 features
        for i, feature in enumerate(features, 1):
            template += f"- **{feature}**: [Business impact with metric]\n"

        template += f"""

## 🛠️ Technical Architecture

"""

        # Add tech stack information
        tech_stack = analysis['tech_stack']
        for category, technologies in tech_stack.items():
            if technologies:
                template += f"- **{category.title()}**: {', '.join(technologies)}\n"

        template += f"""

## 📊 Results & Metrics

"""

        # Add estimated metrics
        metrics = analysis['metrics']
        for category, items in metrics.items():
            if items:
                template += f"- **{category.replace('_', ' ').title()}**: {len(items)} improvements\n"

        template += """

## 🔗 Live Demo & Source
**Demo**: [Link to deployed version]
**Source**: [Link to GitHub repository]
**Case Study**: [Link to detailed technical breakdown]

---

*Project demonstrates expertise in modern web development, problem-solving, and technical leadership.*
"""

        return template.strip()

    def generate_about_section(self, analysis: Dict[str, Any]) -> str:
        """Generate a professional about section."""
        template = """# Senior Full-Stack Developer

Passionate about building scalable web applications that solve real business problems. With expertise in modern technologies and a focus on clean, maintainable code, I create solutions that deliver exceptional user experiences.

## Technical Expertise

"""

        # Add tech stack from project
        tech_stack = analysis['tech_stack']
        for category, technologies in tech_stack.items():
            if technologies:
                template += f"- **{category.title()}**: {', '.join(technologies)}\n"

        template += """

## Key Achievements

"""

        # Add project-based achievements
        file_analysis = analysis['files']
        template += f"- **Built complex application** with {file_analysis['source_files']}+ source files\n"

        if file_analysis['test_files'] > 0:
            template += f"- **Comprehensive testing** with {file_analysis['test_files']}+ test files\n"

        if analysis['metrics']['performance_improvements']:
            template += "- **Performance optimization** with measurable improvements\n"

        template += """

## Development Philosophy

I believe in:
- **Clean architecture** that scales with requirements
- **Performance optimization** for exceptional user experience
- **Continuous learning** to stay current with emerging technologies
- **Collaborative development** and knowledge sharing

## Let's Connect

Interested in challenging projects that push boundaries? Let's discuss how my expertise can contribute to your goals.

**📧 Email**: [your.email@example.com]
**💼 LinkedIn**: [linkedin.com/in/yourprofile]
**🐙 GitHub**: [github.com/yourusername]
**🌐 Portfolio**: [yourportfolio.com]

---

*"Building the future of web applications, one line of code at a time."*
"""

        return template.strip()

    def generate_blog_post(self, analysis: Dict[str, Any], style: str = "tutorial") -> str:
        """Generate a technical blog post."""
        if style == "tutorial":
            return self._generate_tutorial_post(analysis)
        elif style == "case_study":
            return self._generate_case_study_post(analysis)
        else:
            return self._generate_lessons_learned_post(analysis)

    def _generate_tutorial_post(self, analysis: Dict[str, Any]) -> str:
        """Generate a tutorial-style blog post."""
        tech_stack = analysis['tech_stack']
        main_tech = " ".join(tech_stack.get('frontend', [])[:2] or tech_stack.get('backend', [])[:2])

        template = f"""# Building Modern Applications with {main_tech.title()}

## Introduction

In this tutorial, we'll explore how to build modern web applications using {main_tech}. This approach combines performance optimization with developer productivity to create exceptional user experiences.

## Prerequisites

Before starting, make sure you have:
- Node.js 18+ installed
- Basic knowledge of {main_tech.split()[0]}
- Understanding of web development concepts

## Step 1: Project Setup

Let's start by setting up our project structure:

```bash
# Initialize project
npm init -y
npm install {main_tech}
```

## Step 2: Core Implementation

Here's how we implement the main functionality:

```javascript
// Core implementation example
// Based on {len(analysis['files']['source_files'])}+ source files in this project
```

## Step 3: Performance Optimization

Based on our analysis of {analysis['project_name']}, we implemented several optimizations:

"""

        # Add performance insights
        if analysis['metrics']['performance_improvements']:
            for improvement in analysis['metrics']['performance_improvements'][:3]:
                template += f"- {improvement}\n"

        template += """

## Common Challenges & Solutions

Here are some challenges we encountered and how we solved them:

### Challenge 1: [Specific technical challenge]
**Solution**: [Your approach with code example]

### Challenge 2: [Another technical challenge]
**Solution**: [Your approach with results]

## Best Practices

From our experience building {analysis['project_name']}, here are key takeaways:

- Always consider scalability from the beginning
- Implement comprehensive testing strategies
- Focus on performance optimization
- Maintain clean, readable code

## Conclusion

Building modern applications with {main_tech} requires attention to both technical details and user experience. By following these practices, you can create applications that scale effectively and deliver exceptional performance.

## Next Steps

- Experiment with the provided code examples
- Explore advanced {main_tech} features
- Consider deployment strategies
- Monitor and optimize performance

---

**Live Demo**: [Link to working example]
**Source Code**: [Link to GitHub repository]

*Have questions? Feel free to reach out or leave comments below!*
"""

        return template.strip()

    def _generate_case_study_post(self, analysis: Dict[str, Any]) -> str:
        """Generate a case study blog post."""
        template = f"""# Case Study: How {analysis['project_name'].title()} Achieved [Specific Goal]

## Overview

{analysis['project_name'].title()} is a [project type] that successfully [achieved specific outcome]. This case study explores the technical challenges, implementation approach, and measurable results.

## The Challenge

[Business context and specific problems]

**Key Challenges:**
- Challenge 1 with specific details
- Challenge 2 with business impact
- Challenge 3 with technical complexity

## The Solution

Our approach involved:

### Technical Architecture
"""

        # Add tech stack details
        tech_stack = analysis['tech_stack']
        for category, technologies in tech_stack.items():
            if technologies:
                template += f"- **{category.title()}**: {', '.join(technologies)}\n"

        template += """

### Implementation Strategy

[Detailed approach with technical details]

## Results & Impact

### Quantifiable Metrics
"""

        # Add metrics from analysis
        metrics = analysis['metrics']
        for category, items in metrics.items():
            if items:
                template += f"- **{category.replace('_', ' ').title()}**: {len(items)} improvements\n"

        template += f"""

### Technical Achievements
- Successfully implemented {len(analysis['files']['source_files'])}+ source files
- Comprehensive testing with {len(analysis['files']['test_files'])}+ test files
- Robust architecture supporting scalability

## Lessons Learned

### What Worked Well
1. [Specific success factor]
2. [Another success factor]
3. [Technical decision that paid off]

### Challenges Overcome
1. [Technical challenge and solution]
2. [Business constraint and workaround]
3. [Team/process improvement]

### Recommendations for Similar Projects
1. [Specific technical recommendation]
2. [Process recommendation]
3. [Tool/Framework recommendation]

## Future Considerations

[Plans for improvements and next steps]

---

**Project Repository**: [Link to source code]
**Live Demo**: [Link to deployed application]

*Interested in similar solutions? Let's discuss how we can apply these learnings to your project.*
"""

        return template.strip()

    def _generate_lessons_learned_post(self, analysis: Dict[str, Any]) -> str:
        """Generate a lessons learned blog post."""
        template = f"""# Technical Lessons from Building {analysis['project_name'].title()}

After completing {analysis['project_name'].title()}, I wanted to share the key technical lessons learned during development. These insights might help you avoid similar pitfalls in your projects.

## Project Context

{analysis['project_name'].title()} is a [brief project description] built with:

"""

        # Add tech stack
        tech_stack = analysis['tech_stack']
        for category, technologies in tech_stack.items():
            if technologies:
                template += f"- **{category}**: {', '.join(technologies)}\n"

        template += f"""

## Key Technical Lessons

### 1. Architecture Decisions

**What we did right:**
- Chose scalable architecture from the start
- Implemented proper separation of concerns
- Used appropriate design patterns

**What we'd change:**
- [Specific architectural mistake]
- [Alternative approach for future projects]

### 2. Technology Choices

**Wins:**
- {tech_stack.get('frontend', ['Technology'])[0] if tech_stack.get('frontend') else 'Chosen framework'} proved excellent for our use case
- Integration between frontend and backend was seamless

**Challenges:**
- [Specific technology limitation]
- [Integration difficulty]

### 3. Development Process

**Effective Practices:**
- Commit history shows {len(analysis['commits']['recent_commits'])}+ recent commits
- {len(analysis['commits']['features_added'])} features successfully added
- {len(analysis['commits']['bugs_fixed'])} bugs resolved

**Process Improvements:**
- Better testing strategies needed
- Improved documentation practices
- More robust CI/CD pipeline

## Performance Insights

"""

        # Add performance-related insights
        if analysis['metrics']['performance_improvements']:
            template += "### Performance Optimizations Implemented:\n"
            for improvement in analysis['metrics']['performance_improvements']:
                template += f"- {improvement}\n"

        template += """

### Monitoring and Metrics

What we measured and why it matters:
- [Performance metric 1]
- [Performance metric 2]
- [User experience metric]

## Team and Collaboration

### Communication Patterns
- [What worked well for team communication]
- [Tools that proved effective]
- [Meeting structures that helped]

### Code Quality
- Total of {file_count} files in project
- [Code review practices]
- [Documentation approaches]

## Business vs. Technical Trade-offs

### Decisions That Required Balance
1. [Specific trade-off example]
2. [Another balancing act]
3. [Cost vs. quality decisions]

### How We Decided
- [Decision-making framework]
- [Stakeholder involvement]
- [Technical vs. business priority]

## Tools and Dependencies

**Most Valuable Tools:**
"""

        # Add key dependencies
        deps = analysis['dependencies']
        if deps['frameworks']:
            template += f"- Frameworks: {', '.join(deps['frameworks'][:3])}\n"
        if deps['tools']:
            template += f"- Development tools: {', '.join(deps['tools'][:3])}\n"

        template += """

**Dependencies We'd Reconsider:**
- [Dependency that caused issues]
- [Alternative we discovered]

## Future Improvements

### Technical Debt
- [Areas needing refactoring]
- [Performance opportunities]
- [Security improvements]

### New Features
- [Planned enhancements]
- [Technology upgrades]
- [Architecture evolution]

## Recommendations for Similar Projects

### Before You Start
1. [Specific recommendation]
2. [Warning about common pitfall]
3. [Tool/suggestion]

### During Development
1. [Process recommendation]
2. [Testing strategy]
3. [Best practice to follow]

### After Launch
1. [Monitoring setup]
2. [Maintenance plan]
3. [Scale preparation]

## Conclusion

Building {analysis['project_name'].title()} taught us valuable lessons about [key takeaway]. The combination of [technology 1] and [technology 2] proved [effective/challenging], and our approach to [specific challenge] resulted in [positive outcome].

The most important lesson? [Primary takeaway sentence].

---

**Project Repository**: [Link to source]
**Related Articles**: [Links to other relevant content]

*What lessons have you learned from similar projects? Share your insights in the comments!*
"""

        return template.strip()

    def save_analysis(self, analysis: Dict[str, Any], output_path: str):
        """Save project analysis to file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)

        print(f"✅ Analysis saved to {output_path}")

    def save_content(self, content: str, output_path: str):
        """Save generated content to file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(content)

        print(f"✅ Content saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate portfolio content from project analysis")
    parser.add_argument("command", choices=["analyze", "project-description", "about-section", "blog-post"],
                       help="Command to execute")
    parser.add_argument("--project-path", default=".", help="Path to project directory")
    parser.add_argument("--readme", help="Path to README file")
    parser.add_argument("--commits", help="Path to commit log file")
    parser.add_argument("--tech-stack", help="Path to tech stack data")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--style", default="tutorial", choices=["tutorial", "case_study", "lessons_learned"],
                       help="Blog post style")

    args = parser.parse_args()

    generator = PortfolioContentGenerator(args.project_path)

    if args.command == "analyze":
        analysis = generator.analyze_project()
        generator.save_analysis(analysis, args.output)
        print(f"📊 Project analysis complete!")
        print(f"   - Project: {analysis['project_name']}")
        print(f"   - Technologies: {sum(len(tech) for tech in analysis['tech_stack'].values())}")
        print(f"   - Features: {len(analysis['features'])}")
        print(f"   - Files: {analysis['files']['total_files']}")

    elif args.command == "project-description":
        analysis = generator.analyze_project()
        content = generator.generate_project_description(analysis)
        generator.save_content(content, args.output)
        print("📝 Project description generated!")

    elif args.command == "about-section":
        analysis = generator.analyze_project()
        content = generator.generate_about_section(analysis)
        generator.save_content(content, args.output)
        print("👤 About section generated!")

    elif args.command == "blog-post":
        analysis = generator.analyze_project()
        content = generator.generate_blog_post(analysis, args.style)
        generator.save_content(content, args.output)
        print(f"📚 Blog post generated ({args.style} style)!")


if __name__ == "__main__":
    main()