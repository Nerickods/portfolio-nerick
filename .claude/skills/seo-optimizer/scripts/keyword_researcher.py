#!/usr/bin/env python3
"""
Keyword Researcher for Developer Portfolios
Specialized keyword research and optimization for developer portfolios
"""

import json
import re
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import Counter
import requests


@dataclass
class KeywordData:
    """Keyword data structure"""
    keyword: str
    volume: int  # Monthly search volume
    difficulty: float  # Competition difficulty (0-100)
    relevance: float  # Relevance to developer portfolio (0-100)
    category: str  # Category: technical, location, experience, industry


class KeywordResearcher:
    """Specialized keyword researcher for developer portfolios"""

    def __init__(self):
        # Technical keywords with search volume estimates
        self.technical_keywords = {
            # Frontend
            'react developer': 1200, 'react developer new york': 800, 'react developer remote': 600,
            'react developer san francisco': 500, 'react developer london': 450,
            'next.js developer': 800, 'next.js developer remote': 400, 'next.js portfolio': 300,
            'vue.js developer': 600, 'angular developer': 700, 'frontend developer': 2000,
            'javascript developer': 1500, 'typescript developer': 900, 'html css developer': 800,

            # Backend
            'node.js developer': 1400, 'python developer': 1800, 'django developer': 600,
            'flask developer': 400, 'express.js developer': 700, 'backend developer': 1600,
            'api developer': 800, 'rest api developer': 500, 'graphql developer': 400,

            # Full Stack
            'full stack developer': 2200, 'full stack javascript developer': 1000,
            'mern stack developer': 600, 'mean stack developer': 400, 'full stack remote': 800,
            'full stack developer new york': 700, 'full stack developer san francisco': 600,

            # Mobile
            'react native developer': 800, 'flutter developer': 600, 'ios developer': 900,
            'android developer': 1000, 'mobile app developer': 1200,

            # DevOps
            'devops engineer': 1800, 'aws developer': 1400, 'docker developer': 800,
            'kubernetes developer': 900, 'cloud developer': 1000, 'site reliability engineer': 700,

            # Database
            'mongodb developer': 500, 'postgresql developer': 600, 'mysql developer': 700,
            'database developer': 800, 'sql developer': 900,

            # General
            'web developer': 2500, 'software engineer': 3000, 'software developer': 2400,
            'programmer': 1800, 'coder': 1200
        }

        # Experience level keywords
        self.experience_keywords = {
            'junior developer': 800, 'entry level developer': 600, 'beginner developer': 400,
            'mid-level developer': 700, 'mid level developer': 600, 'senior developer': 1500,
            'lead developer': 900, 'principal developer': 600, 'staff developer': 500,
            'senior software engineer': 1200, 'senior web developer': 800
        }

        # Location keywords
        self.location_keywords = {
            'developer new york': 1200, 'developer nyc': 800, 'developer manhattan': 400,
            'developer san francisco': 1000, 'developer sf': 600, 'developer bay area': 500,
            'developer london': 900, 'developer remote': 1800, 'developer work from home': 800,
            'developer los angeles': 700, 'developer la': 500, 'developer chicago': 600,
            'developer boston': 500, 'developer seattle': 600, 'developer austin': 500,
            'developer denver': 400, 'developer portland': 300, 'developer miami': 400
        }

        # Industry keywords
        self.industry_keywords = {
            'fintech developer': 400, 'healthtech developer': 300, 'edtech developer': 200,
            'e-commerce developer': 500, 'ecommerce developer': 400, 'saas developer': 600,
            'startup developer': 800, 'enterprise developer': 700, 'agency developer': 500,
            'freelance developer': 1200, 'contract developer': 800, 'consultant developer': 600
        }

        # Technology-specific combinations
        self.tech_combinations = [
            ('react', 'node.js'), ('react', 'python'), ('react', 'typescript'),
            ('vue.js', 'node.js'), ('angular', 'node.js'), ('next.js', 'graphql'),
            ('python', 'django'), ('python', 'flask'), ('javascript', 'node.js'),
            ('typescript', 'react'), ('typescript', 'node.js'), ('aws', 'node.js'),
            ('docker', 'node.js'), ('kubernetes', 'react'), ('mongodb', 'node.js')
        ]

    def research_keywords(self, content: str, location: str = None, technologies: List[str] = None) -> Dict:
        """Research keywords based on portfolio content and preferences"""

        content_lower = content.lower()

        # Analyze existing content
        existing_keywords = self._extract_existing_keywords(content_lower)

        # Generate keyword suggestions
        keyword_suggestions = self._generate_keyword_suggestions(
            existing_keywords, location, technologies
        )

        # Analyze competition
        competitor_analysis = self._analyze_competition(existing_keywords)

        # Calculate keyword opportunities
        opportunities = self._identify_opportunities(keyword_suggestions, competitor_analysis)

        return {
            'existing_keywords': existing_keywords,
            'keyword_suggestions': keyword_suggestions,
            'competitor_analysis': competitor_analysis,
            'opportunities': opportunities,
            'content_gaps': self._identify_content_gaps(existing_keywords)
        }

    def _extract_existing_keywords(self, content: str) -> Dict:
        """Extract existing keywords from portfolio content"""

        found_keywords = {
            'technical': [],
            'experience': [],
            'location': [],
            'industry': []
        }

        content_words = set(content.split())

        # Find technical keywords
        for keyword in self.technical_keywords:
            if keyword in content:
                found_keywords['technical'].append({
                    'keyword': keyword,
                    'volume': self.technical_keywords[keyword],
                    'found_in_content': True
                })

        # Find experience level keywords
        for keyword in self.experience_keywords:
            if keyword in content:
                found_keywords['experience'].append({
                    'keyword': keyword,
                    'volume': self.experience_keywords[keyword],
                    'found_in_content': True
                })

        # Find location keywords
        for keyword in self.location_keywords:
            if keyword in content:
                found_keywords['location'].append({
                    'keyword': keyword,
                    'volume': self.location_keywords[keyword],
                    'found_in_content': True
                })

        # Find industry keywords
        for keyword in self.industry_keywords:
            if keyword in content:
                found_keywords['industry'].append({
                    'keyword': keyword,
                    'volume': self.industry_keywords[keyword],
                    'found_in_content': True
                })

        return found_keywords

    def _generate_keyword_suggestions(self, existing_keywords: Dict, location: str = None, technologies: List[str] = None) -> Dict:
        """Generate keyword suggestions based on portfolio and preferences"""

        suggestions = {
            'primary': [],  # High volume, high relevance
            'secondary': [],  # Medium volume, good relevance
            'long_tail': [],  # Low volume, very specific
            'location_based': [],
            'technology_specific': []
        }

        # Primary keywords (high volume searches)
        primary_base = [
            'full stack developer', 'react developer', 'node.js developer',
            'python developer', 'frontend developer', 'backend developer'
        ]

        for base in primary_base:
            if base in self.technical_keywords:
                suggestions['primary'].append({
                    'keyword': base,
                    'volume': self.technical_keywords[base],
                    'difficulty': self._estimate_difficulty(base),
                    'relevance': 95,
                    'reason': 'High volume search term with strong relevance'
                })

        # Add location-specific keywords
        if location:
            location_lower = location.lower()
            for loc_keyword, volume in self.location_keywords.items():
                if location_lower in loc_keyword or loc_keyword in location_lower:
                    suggestions['location_based'].append({
                        'keyword': loc_keyword,
                        'volume': volume,
                        'difficulty': self._estimate_difficulty(loc_keyword),
                        'relevance': 90,
                        'reason': 'Targeted local search term'
                    })

        # Technology-specific combinations
        if technologies:
            for tech in technologies:
                tech_lower = tech.lower()
                # Find base technical keywords
                for tech_keyword, volume in self.technical_keywords.items():
                    if tech_lower in tech_keyword:
                        suggestions['technology_specific'].append({
                            'keyword': tech_keyword,
                            'volume': volume,
                            'difficulty': self._estimate_difficulty(tech_keyword),
                            'relevance': 85,
                            'reason': f'Matches your {tech} expertise'
                        })

        # Generate technology combination keywords
        for tech1, tech2 in self.tech_combinations:
            if technologies and (tech1 in [t.lower() for t in technologies] or
                               tech2 in [t.lower() for t in technologies]):
                combo_keyword = f"{tech1} {tech2} developer"
                estimated_volume = min(self.technical_keywords.get(f"{tech1} developer", 500),
                                     self.technical_keywords.get(f"{tech2} developer", 500)) // 2

                suggestions['secondary'].append({
                    'keyword': combo_keyword,
                    'volume': estimated_volume,
                    'difficulty': self._estimate_difficulty(combo_keyword),
                    'relevance': 80,
                    'reason': f'Combines {tech1} and {tech2} skills'
                })

        # Long-tail keywords (very specific)
        long_tail_patterns = [
            'react developer for startups',
            'node.js api developer',
            'python data engineer',
            'typescript react developer',
            'full stack javascript freelancer',
            'remote react developer',
            'senior python backend developer',
            'next.js frontend developer'
        ]

        for pattern in long_tail_patterns:
            if not any(existing['keyword'] == pattern for existing in existing_keywords['technical']):
                suggestions['long_tail'].append({
                    'keyword': pattern,
                    'volume': 100,  # Estimated lower volume
                    'difficulty': 30,  # Lower competition
                    'relevance': 75,
                    'reason': 'Specific skill combination with lower competition'
                })

        return suggestions

    def _analyze_competition(self, existing_keywords: Dict) -> Dict:
        """Analyze keyword competition (simulated)"""

        competition_analysis = {
            'high_competition': [],
            'medium_competition': [],
            'low_competition': [],
            'opportunity_keywords': []
        }

        # Analyze competition for different keyword types
        all_keywords = []

        # Add existing keywords to analysis
        for category, keywords in existing_keywords.items():
            for keyword_data in keywords:
                all_keywords.append((keyword_data['keyword'], keyword_data['volume'], category))

        # Add some common high-competition keywords
        high_comp_keywords = [
            'web developer', 'software engineer', 'react developer',
            'full stack developer', 'javascript developer'
        ]

        for keyword in high_comp_keywords:
            volume = self.technical_keywords.get(keyword, 1000)
            competition_analysis['high_competition'].append({
                'keyword': keyword,
                'estimated_competition': 85,
                'volume': volume,
                'difficulty': 'High'
            })

        # Medium competition keywords
        medium_comp_keywords = [
            'vue.js developer', 'angular developer', 'python django developer',
            'node.js api developer', 'typescript developer'
        ]

        for keyword in medium_comp_keywords:
            volume = self.technical_keywords.get(keyword, 600)
            competition_analysis['medium_competition'].append({
                'keyword': keyword,
                'estimated_competition': 60,
                'volume': volume,
                'difficulty': 'Medium'
            })

        # Low competition (long-tail) keywords
        low_comp_keywords = [
            'react graphql developer', 'next.js mongodb developer',
            'python flask api developer', 'vue.js firebase developer',
            'docker kubernetes developer'
        ]

        for keyword in low_comp_keywords:
            competition_analysis['low_competition'].append({
                'keyword': keyword,
                'estimated_competition': 30,
                'volume': 200,
                'difficulty': 'Low'
            })

        # Identify opportunity keywords (good volume, lower competition)
        opportunity_keywords = [
            'next.js developer remote',
            'react typescript developer',
            'python flask developer',
            'vue.js node.js developer',
            'full stack mongodb developer'
        ]

        for keyword in opportunity_keywords:
            volume = 400  # Estimated
            competition_analysis['opportunity_keywords'].append({
                'keyword': keyword,
                'estimated_competition': 45,
                'volume': volume,
                'opportunity_score': 75,  # Volume / Competition ratio
                'reason': 'Good search volume with moderate competition'
            })

        return competition_analysis

    def _identify_opportunities(self, suggestions: Dict, competition: Dict) -> List[Dict]:
        """Identify keyword optimization opportunities"""

        opportunities = []

        # High volume, low competition opportunities
        for keyword_data in suggestions['primary']:
            if keyword_data['volume'] > 1000:
                opportunities.append({
                    'type': 'high_volume_opportunity',
                    'keyword': keyword_data['keyword'],
                    'priority': 'High',
                    'action': f'Create dedicated content around "{keyword_data["keyword"]}"',
                    'estimated_traffic': keyword_data['volume'],
                    'difficulty': keyword_data['difficulty']
                })

        # Location-based opportunities
        for keyword_data in suggestions['location_based']:
            if keyword_data['volume'] > 400:
                opportunities.append({
                    'type': 'location_opportunity',
                    'keyword': keyword_data['keyword'],
                    'priority': 'High' if keyword_data['volume'] > 800 else 'Medium',
                    'action': f'Add location-specific content for "{keyword_data["keyword"]}"',
                    'estimated_traffic': keyword_data['volume'],
                    'difficulty': keyword_data['difficulty']
                })

        # Long-tail opportunities (easier to rank for)
        for keyword_data in suggestions['long_tail']:
            opportunities.append({
                'type': 'long_tail_opportunity',
                'keyword': keyword_data['keyword'],
                'priority': 'Medium',
                'action': f'Create specific project pages targeting "{keyword_data["keyword"]}"',
                'estimated_traffic': keyword_data['volume'],
                'difficulty': 30  # Lower difficulty for long-tail
            })

        # Technology combination opportunities
        for keyword_data in suggestions['technology_specific']:
            if keyword_data['volume'] > 500:
                opportunities.append({
                    'type': 'tech_combination_opportunity',
                    'keyword': keyword_data['keyword'],
                    'priority': 'Medium',
                    'action': f'Highlight {keyword_data["keyword"]} experience in portfolio',
                    'estimated_traffic': keyword_data['volume'],
                    'difficulty': keyword_data['difficulty']
                })

        # Sort by priority and potential impact
        opportunities.sort(key=lambda x: (x['priority'] == 'High', x['estimated_traffic']), reverse=True)

        return opportunities

    def _identify_content_gaps(self, existing_keywords: Dict) -> List[str]:
        """Identify content gaps in current keyword coverage"""

        gaps = []

        # Check for missing major keywords
        major_keywords = [
            'full stack developer', 'react developer', 'node.js developer',
            'python developer', 'frontend developer', 'backend developer'
        ]

        found_major = [kw['keyword'] for kw in existing_keywords['technical']]

        for major in major_keywords:
            if major not in found_major:
                gaps.append(f"Missing high-volume keyword: '{major}'")

        # Check for experience level keywords
        experience_found = [kw['keyword'] for kw in existing_keywords['experience']]
        if not experience_found:
            gaps.append("No experience level keywords (junior, senior, etc.)")

        # Check for location keywords
        location_found = [kw['keyword'] for kw in existing_keywords['location']]
        if not location_found:
            gaps.append("No location-based keywords for local search")

        # Check for industry keywords
        industry_found = [kw['keyword'] for kw in existing_keywords['industry']]
        if not industry_found:
            gaps.append("No industry-specific keywords (fintech, startup, etc.)")

        # Check for technology combinations
        tech_combinations_missing = []
        found_tech = [kw['keyword'] for kw in existing_keywords['technical']]

        for tech1, tech2 in self.tech_combinations:
            combo = f"{tech1} {tech2}"
            if not any(combo in found or tech1 in found or tech2 in found for found in found_tech):
                tech_combinations_missing.append(combo)

        if tech_combinations_missing:
            gaps.append(f"Missing technology combinations: {', '.join(tech_combinations_missing[:3])}")

        return gaps

    def _estimate_difficulty(self, keyword: str) -> float:
        """Estimate keyword difficulty (0-100)"""

        # Base difficulty on search volume
        base_difficulty = 30

        if keyword in self.technical_keywords:
            volume = self.technical_keywords[keyword]
        elif keyword in self.experience_keywords:
            volume = self.experience_keywords[keyword]
        elif keyword in self.location_keywords:
            volume = self.location_keywords[keyword]
        elif keyword in self.industry_keywords:
            volume = self.industry_keywords[keyword]
        else:
            volume = 200  # Default estimate

        # Higher volume = higher difficulty
        if volume > 2000:
            difficulty = 85
        elif volume > 1500:
            difficulty = 75
        elif volume > 1000:
            difficulty = 65
        elif volume > 500:
            difficulty = 50
        elif volume > 200:
            difficulty = 35
        else:
            difficulty = 25

        # Adjust for keyword type
        if any(indicator in keyword.lower() for indicator in ['remote', 'freelance', 'contract']):
            difficulty -= 10  # Lower competition for remote/freelance

        if any(indicator in keyword.lower() for indicator in ['senior', 'lead', 'principal']):
            difficulty += 5  # Higher competition for senior roles

        return max(0, min(100, difficulty))

    def generate_keyword_report(self, research_results: Dict) -> str:
        """Generate a comprehensive keyword research report"""

        report = []
        report.append("=" * 60)
        report.append("🔍 KEYWORD RESEARCH REPORT")
        report.append("=" * 60)

        # Summary
        total_existing = sum(len(keywords) for keywords in research_results['existing_keywords'].values())
        report.append(f"\n📊 SUMMARY")
        report.append(f"Existing Keywords Found: {total_existing}")
        report.append(f"Top Opportunities: {len(research_results['opportunities'])}")

        # Existing keywords
        report.append("\n🎯 EXISTING KEYWORDS")
        report.append("-" * 25)

        for category, keywords in research_results['existing_keywords'].items():
            if keywords:
                report.append(f"\n{category.title()} Keywords:")
                for keyword in keywords[:5]:  # Show top 5
                    report.append(f"  • {keyword['keyword']} ({keyword['volume']}/month)")

        # Top opportunities
        report.append("\n🚀 TOP OPTIMIZATION OPPORTUNITIES")
        report.append("-" * 37)

        for i, opportunity in enumerate(research_results['opportunities'][:5], 1):
            report.append(f"\n{i}. {opportunity['keyword']}")
            report.append(f"   Priority: {opportunity['priority']}")
            report.append(f"   Estimated Traffic: {opportunity['estimated_traffic']}/month")
            report.append(f"   Action: {opportunity['action']}")

        # Content gaps
        if research_results['content_gaps']:
            report.append("\n⚠️  CONTENT GAPS")
            report.append("-" * 18)
            for gap in research_results['content_gaps']:
                report.append(f"  • {gap}")

        # Recommendations
        report.append("\n💡 RECOMMENDATIONS")
        report.append("-" * 20)

        recommendations = [
            "1. Add your location to attract local opportunities",
            "2. Include experience level keywords (senior, junior, etc.)",
            "3. Highlight technology combinations you work with",
            "4. Create project-specific pages with detailed descriptions",
            "5. Target industry-specific keywords if you have domain expertise",
            "6. Consider remote work keywords for broader opportunities"
        ]

        for rec in recommendations:
            report.append(f"  {rec}")

        return "\n".join(report)


def main():
    """Example usage of the keyword researcher"""

    # Example portfolio content
    sample_content = """
    I am a software developer with experience in React, Node.js, and Python.
    I have worked on web applications using JavaScript and TypeScript.
    Currently looking for opportunities as a frontend developer.
    """

    researcher = KeywordResearcher()
    results = researcher.research_keywords(
        content=sample_content,
        location="New York",
        technologies=["React", "Node.js", "Python"]
    )

    report = researcher.generate_keyword_report(results)
    print(report)


if __name__ == "__main__":
    main()