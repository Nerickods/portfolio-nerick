#!/usr/bin/env python3
"""
Meta Tag Generator for Developer Portfolios
Generate optimized meta tags, OpenGraph, and Twitter Card tags
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class MetaTags:
    """Generated meta tags structure"""
    title: str
    description: str
    keywords: str
    canonical_url: str
    og_tags: Dict
    twitter_tags: Dict
    structured_data: Dict
    additional_tags: List[Dict]


class MetaTagGenerator:
    """Specialized meta tag generator for developer portfolios"""

    def __init__(self):
        self.dev_keywords = [
            'developer', 'engineer', 'software engineer', 'web developer',
            'full stack', 'frontend', 'backend', 'mobile developer',
            'react', 'node.js', 'python', 'javascript', 'typescript'
        ]

        self.title_templates = [
            "{name} | {title} in {location}",
            "{name} - {title} | {technologies}",
            "{title} | {name} | {specialization}",
            "{name} | {technologies} Developer | {location}",
            "{title} & {technologies} | {name} | Portfolio"
        ]

        self.description_templates = [
            "{experience} {title} specializing in {technologies}. {bio} Available for {work_type} in {location}.",
            "Skilled {title} with {years} years experience in {technologies}. {bio} Located in {location}, seeking {opportunities}.",
            "{experience} {title} creating {achievements} using {technologies}. {bio} {location-based}.",
            "Passionate {title} with expertise in {technologies}. {bio} {call_to_action} from {location}.",
            "{title} focused on {specialization} with strong skills in {technologies}. {bio} {location}."
        ]

    def generate_meta_tags(self, portfolio_data: Dict) -> MetaTags:
        """Generate comprehensive meta tags for a developer portfolio"""

        # Extract data
        name = portfolio_data.get('name', 'Developer')
        title = portfolio_data.get('title', 'Software Developer')
        location = portfolio_data.get('location', '')
        technologies = portfolio_data.get('technologies', [])
        experience = portfolio_data.get('experience_level', '')
        bio = portfolio_data.get('bio', '')
        url = portfolio_data.get('url', '')
        image_url = portfolio_data.get('image_url', '')
        github = portfolio_data.get('github', '')
        linkedin = portfolio_data.get('linkedin', '')
        years_experience = portfolio_data.get('years_experience', '')
        work_type = portfolio_data.get('work_type', 'opportunities')
        achievements = portfolio_data.get('achievements', '')

        # Generate optimized title
        title_tag = self._generate_title(name, title, location, technologies)

        # Generate optimized description
        description = self._generate_description(
            experience, title, technologies, bio, location, work_type,
            years_experience, achievements
        )

        # Generate keywords
        keywords = self._generate_keywords(title, technologies, experience, location)

        # OpenGraph tags
        og_tags = self._generate_og_tags(
            title_tag, description, url, image_url, name, title
        )

        # Twitter Card tags
        twitter_tags = self._generate_twitter_tags(
            title_tag, description, image_url, name
        )

        # Structured data
        structured_data = self._generate_structured_data(
            portfolio_data, title_tag, description, url
        )

        # Additional meta tags
        additional_tags = self._generate_additional_tags(
            url, technologies, location
        )

        return MetaTags(
            title=title_tag,
            description=description,
            keywords=keywords,
            canonical_url=url,
            og_tags=og_tags,
            twitter_tags=twitter_tags,
            structured_data=structured_data,
            additional_tags=additional_tags
        )

    def _generate_title(self, name: str, title: str, location: str, technologies: List[str]) -> str:
        """Generate optimized title tag"""

        # Limit technologies to top 2-3 most important
        top_techs = technologies[:3] if technologies else []

        # Choose best template based on available data
        if location and top_techs:
            template = self.title_templates[0]  # Name | Title in Location
            formatted = template.format(
                name=name,
                title=title,
                location=location
            )
        elif top_techs:
            template = self.title_templates[1]  # Name - Title | Technologies
            techs_str = ", ".join(top_techs)
            formatted = template.format(
                name=name,
                title=title,
                technologies=techs_str
            )
        elif location:
            template = self.title_templates[0]
            formatted = template.format(
                name=name,
                title=title,
                location=location
            )
        else:
            formatted = f"{name} | {title} | Portfolio"

        # Ensure length is optimal (50-60 characters)
        if len(formatted) > 60:
            if len(formatted) > 70:
                # Truncate more aggressively
                if location:
                    formatted = f"{name} | {title} | {location[:20]}"
                else:
                    formatted = f"{name} | {title} Developer"
            else:
                # Minor truncation
                formatted = formatted[:57] + "..."

        return formatted

    def _generate_description(self, experience: str, title: str, technologies: List[str],
                            bio: str, location: str, work_type: str,
                            years_experience: str, achievements: str) -> str:
        """Generate optimized meta description"""

        techs_str = ", ".join(technologies[:5]) if technologies else "modern technologies"

        # Build bio snippet
        bio_snippet = bio[:80] + "..." if len(bio) > 80 else bio

        # Build achievements snippet
        achievements_snippet = achievements[:60] + "..." if len(achievements) > 60 else achievements

        # Choose template based on available data
        if experience and years_experience:
            template = self.description_templates[0]
            description = template.format(
                experience=experience,
                title=title,
                technologies=techs_str,
                bio=bio_snippet,
                work_type=work_type,
                location=location
            )
        elif achievements:
            template = self.description_templates[2]
            description = template.format(
                experience=experience or "Skilled",
                title=title,
                achievements=achievements_snippet,
                technologies=techs_str,
                bio=bio_snippet,
                location=location
            )
        else:
            template = self.description_templates[3]
            description = template.format(
                title=title,
                technologies=techs_str,
                bio=bio_snippet,
                call_to_action=f"Open to {work_type}" if work_type else "Open to opportunities",
                location=location
            )

        # Ensure optimal length (120-160 characters)
        if len(description) > 160:
            if len(description) > 180:
                # More aggressive truncation
                description = f"{experience or 'Skilled'} {title} specializing in {techs_str}. {bio_snippet[:50]}... Available for {work_type}."
            else:
                description = description[:157] + "..."

        return description

    def _generate_keywords(self, title: str, technologies: List[str],
                          experience: str, location: str) -> str:
        """Generate keywords meta tag"""

        keywords = []

        # Add title variations
        keywords.append(title)
        keywords.append(title.replace(" ", ""))
        keywords.append(title.replace("Developer", "Engineer"))
        keywords.append(title.replace("Engineer", "Developer"))

        # Add technologies
        for tech in technologies:
            keywords.append(tech)
            keywords.append(f"{tech} developer")
            keywords.append(f"{tech} engineer")

        # Add experience level
        if experience:
            keywords.append(experience)
            keywords.append(f"{experience} developer")
            keywords.append(f"{experience} engineer")

        # Add location
        if location:
            keywords.append(f"developer {location}")
            keywords.append(f"{title} {location}")

        # Add general terms
        keywords.extend([
            'software developer', 'web developer', 'software engineer',
            'full stack developer', 'frontend developer', 'backend developer'
        ])

        # Remove duplicates and limit to most important
        unique_keywords = list(dict.fromkeys(keywords))[:15]

        return ", ".join(unique_keywords)

    def _generate_og_tags(self, title: str, description: str, url: str,
                          image_url: str, name: str, title_role: str) -> Dict:
        """Generate OpenGraph meta tags"""

        og_tags = {
            'og:title': title,
            'og:description': description,
            'og:type': 'website',
            'og:url': url,
            'og:site_name': f"{name}'s Portfolio",
            'og:locale': 'en_US'
        }

        if image_url:
            og_tags.update({
                'og:image': image_url,
                'og:image:alt': f"{name} - {title_role}",
                'og:image:width': '1200',
                'og:image:height': '630'
            })

        # Add professional profile tags
        og_tags.update({
            'profile:first_name': name.split()[0] if name else '',
            'profile:last_name': " ".join(name.split()[1:]) if len(name.split()) > 1 else '',
            'profile:username': name.lower().replace(" ", ""),
        })

        return og_tags

    def _generate_twitter_tags(self, title: str, description: str,
                             image_url: str, name: str) -> Dict:
        """Generate Twitter Card meta tags"""

        twitter_tags = {
            'twitter:card': 'summary_large_image',
            'twitter:title': title,
            'twitter:description': description,
            'twitter:site': '@' + name.lower().replace(" ", ""),  # Assuming Twitter handle
            'twitter:creator': '@' + name.lower().replace(" ", "")
        }

        if image_url:
            twitter_tags['twitter:image'] = image_url

        return twitter_tags

    def _generate_structured_data(self, portfolio_data: Dict,
                                 title: str, description: str, url: str) -> Dict:
        """Generate JSON-LD structured data"""

        name = portfolio_data.get('name', 'Developer')
        title_role = portfolio_data.get('title', 'Software Developer')
        location = portfolio_data.get('location', '')
        email = portfolio_data.get('email', '')
        phone = portfolio_data.get('phone', '')
        github = portfolio_data.get('github', '')
        linkedin = portfolio_data.get('linkedin', '')
        skills = portfolio_data.get('technologies', [])
        projects = portfolio_data.get('projects', [])
        education = portfolio_data.get('education', [])
        work_experience = portfolio_data.get('work_experience', [])
        years_experience = portfolio_data.get('years_experience', '')

        # Person structured data
        person_data = {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": name,
            "jobTitle": title_role,
            "description": description,
            "url": url,
            "knowsAbout": skills[:10]  # Limit to top 10 skills
        }

        # Add contact information
        if email:
            person_data["email"] = email
        if phone:
            person_data["telephone"] = phone

        # Add social profiles
        same_as = []
        if github:
            same_as.append(f"https://github.com/{github}")
        if linkedin:
            same_as.append(f"https://linkedin.com/in/{linkedin}")
        if url:
            same_as.append(url)

        if same_as:
            person_data["sameAs"] = same_as

        # Add location
        if location:
            person_data["address"] = {
                "@type": "PostalAddress",
                "addressLocality": location
            }

        # Add work experience
        if work_experience:
            person_data["hasOccupation"] = {
                "@type": "Occupation",
                "description": title_role,
                "name": title_role,
                "occupationLocation": {
                    "@type": "Place",
                    "address": location
                }
            }

        # Combine with other structured data
        structured_data = [person_data]

        # Add website structured data
        website_data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": f"{name}'s Portfolio",
            "url": url,
            "description": description,
            "author": {
                "@type": "Person",
                "name": name
            }
        }

        structured_data.append(website_data)

        # Add project structured data if available
        for project in projects[:3]:  # Limit to 3 most recent projects
            project_data = {
                "@context": "https://schema.org",
                "@type": "Project",
                "name": project.get('name', ''),
                "description": project.get('description', ''),
                "url": project.get('url', ''),
                "programmingLanguage": project.get('technologies', []),
                "author": {
                    "@type": "Person",
                    "name": name
                }
            }
            structured_data.append(project_data)

        return structured_data

    def _generate_additional_tags(self, url: str, technologies: List[str],
                                location: str) -> List[Dict]:
        """Generate additional meta tags"""

        additional_tags = []

        # Canonical URL
        if url:
            additional_tags.append({
                'tag': 'link',
                'rel': 'canonical',
                'href': url
            })

        # Viewport
        additional_tags.append({
            'tag': 'meta',
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        })

        # Robots
        additional_tags.append({
            'tag': 'meta',
            'name': 'robots',
            'content': 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1'
        })

        # Language
        additional_tags.append({
            'tag': 'meta',
            'http-equiv': 'content-language',
            'content': 'en'
        })

        # Content type
        additional_tags.append({
            'tag': 'meta',
            'http-equiv': 'content-type',
            'content': 'text/html; charset=UTF-8'
        })

        # Theme color
        additional_tags.append({
            'tag': 'meta',
            'name': 'theme-color',
            'content': '#317EFB'  # Default blue color
        })

        # Application name
        additional_tags.append({
            'tag': 'meta',
            'name': 'application-name',
            'content': 'Developer Portfolio'
        })

        # Author
        additional_tags.append({
            'tag': 'meta',
            'name': 'author',
            'content': 'Generated by SEO Optimizer'
        })

        # Generator
        additional_tags.append({
            'tag': 'meta',
            'name': 'generator',
            'content': 'SEO Optimizer for Developer Portfolios'
        })

        # Geo position if location is available
        if location:
            # This would ideally use a geocoding service to get coordinates
            additional_tags.append({
                'tag': 'meta',
                'name': 'geo.placename',
                'content': location
            })

        return additional_tags

    def generate_html_meta_tags(self, meta_tags: MetaTags) -> str:
        """Generate HTML meta tags string"""

        html_tags = []

        # Basic meta tags
        html_tags.append(f'    <title>{meta_tags.title}</title>')
        html_tags.append(f'    <meta name="description" content="{meta_tags.description}">')
        html_tags.append(f'    <meta name="keywords" content="{meta_tags.keywords}">')

        # Canonical URL
        if meta_tags.canonical_url:
            html_tags.append(f'    <link rel="canonical" href="{meta_tags.canonical_url}">')

        # OpenGraph tags
        for property_name, content in meta_tags.og_tags.items():
            html_tags.append(f'    <meta property="{property_name}" content="{content}">')

        # Twitter Card tags
        for name, content in meta_tags.twitter_tags.items():
            html_tags.append(f'    <meta name="{name}" content="{content}">')

        # Additional tags
        for tag_data in meta_tags.additional_tags:
            if tag_data['tag'] == 'meta':
                if 'http-equiv' in tag_data:
                    html_tags.append(f'    <meta http-equiv="{tag_data["http-equiv"]}" content="{tag_data["content"]}">')
                else:
                    html_tags.append(f'    <meta name="{tag_data["name"]}" content="{tag_data["content"]}">')
            elif tag_data['tag'] == 'link':
                html_tags.append(f'    <link rel="{tag_data["rel"]}" href="{tag_data["href"]}">')

        # Structured data
        if meta_tags.structured_data:
            if isinstance(meta_tags.structured_data, list):
                for schema in meta_tags.structured_data:
                    schema_json = json.dumps(schema, indent=2)
                    html_tags.append('    <script type="application/ld+json">')
                    html_tags.append(f'      {schema_json}')
                    html_tags.append('    </script>')
            else:
                schema_json = json.dumps(meta_tags.structured_data, indent=2)
                html_tags.append('    <script type="application/ld+json">')
                html_tags.append(f'      {schema_json}')
                html_tags.append('    </script>')

        return "\n".join(html_tags)

    def generate_json_output(self, meta_tags: MetaTags) -> str:
        """Generate JSON output for the meta tags"""

        output = {
            "meta_tags": {
                "title": meta_tags.title,
                "description": meta_tags.description,
                "keywords": meta_tags.keywords,
                "canonical_url": meta_tags.canonical_url
            },
            "open_graph": meta_tags.og_tags,
            "twitter_card": meta_tags.twitter_tags,
            "structured_data": meta_tags.structured_data,
            "additional_tags": meta_tags.additional_tags,
            "optimization_score": self._calculate_optimization_score(meta_tags)
        }

        return json.dumps(output, indent=2)

    def _calculate_optimization_score(self, meta_tags: MetaTags) -> Dict:
        """Calculate optimization score for the generated meta tags"""

        score = 0
        max_score = 100
        feedback = []

        # Title optimization (25 points)
        title = meta_tags.title
        if 50 <= len(title) <= 60:
            score += 15
            feedback.append("✅ Title length is optimal (50-60 chars)")
        elif 40 <= len(title) <= 70:
            score += 10
            feedback.append("⚠️  Title length is acceptable (40-70 chars)")
        else:
            feedback.append("❌ Title length needs optimization")

        if any(keyword in title.lower() for keyword in ['developer', 'engineer']):
            score += 10
            feedback.append("✅ Title contains relevant keywords")

        # Description optimization (25 points)
        description = meta_tags.description
        if 120 <= len(description) <= 160:
            score += 15
            feedback.append("✅ Description length is optimal (120-160 chars)")
        elif 100 <= len(description) <= 180:
            score += 10
            feedback.append("⚠️  Description length is acceptable (100-180 chars)")
        else:
            feedback.append("❌ Description length needs optimization")

        if description and len(description.split()) >= 15:
            score += 10
            feedback.append("✅ Description has sufficient content")

        # OpenGraph optimization (20 points)
        required_og = ['og:title', 'og:description', 'og:type', 'og:url']
        missing_og = [og for og in required_og if og not in meta_tags.og_tags]

        if not missing_og:
            score += 15
            feedback.append("✅ All essential OpenGraph tags present")
        else:
            feedback.append(f"❌ Missing OpenGraph tags: {', '.join(missing_og)}")

        if 'og:image' in meta_tags.og_tags:
            score += 5
            feedback.append("✅ OpenGraph image present")

        # Twitter Card optimization (15 points)
        required_twitter = ['twitter:card', 'twitter:title', 'twitter:description']
        missing_twitter = [tc for tc in required_twitter if tc not in meta_tags.twitter_tags]

        if not missing_twitter:
            score += 10
            feedback.append("✅ Essential Twitter Card tags present")
        else:
            feedback.append(f"❌ Missing Twitter Card tags: {', '.join(missing_twitter)}")

        if 'twitter:image' in meta_tags.twitter_tags:
            score += 5
            feedback.append("✅ Twitter Card image present")

        # Structured data optimization (15 points)
        if meta_tags.structured_data:
            score += 10
            feedback.append("✅ Structured data present")

            if isinstance(meta_tags.structured_data, list) and len(meta_tags.structured_data) >= 2:
                score += 5
                feedback.append("✅ Multiple structured data types present")
        else:
            feedback.append("❌ No structured data found")

        return {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100),
            "feedback": feedback
        }


def main():
    """Example usage of the meta tag generator"""

    # Example portfolio data
    portfolio_data = {
        "name": "John Doe",
        "title": "Full Stack Developer",
        "location": "San Francisco, CA",
        "technologies": ["React", "Node.js", "TypeScript", "Python"],
        "experience_level": "Senior",
        "bio": "Passionate full stack developer with 8 years of experience building scalable web applications.",
        "url": "https://johndoe.dev",
        "image_url": "https://johndoe.dev/images/profile.jpg",
        "github": "johndoe",
        "linkedin": "johndoe",
        "years_experience": "8+",
        "work_type": "full-time and contract opportunities",
        "achievements": "Led development of 10+ production applications serving millions of users",
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Full-stack e-commerce solution with React and Node.js",
                "url": "https://github.com/johndoe/ecommerce",
                "technologies": ["React", "Node.js", "MongoDB"]
            }
        ]
    }

    generator = MetaTagGenerator()
    meta_tags = generator.generate_meta_tags(portfolio_data)

    # Generate HTML output
    html_tags = generator.generate_html_meta_tags(meta_tags)
    print("Generated HTML Meta Tags:")
    print("=" * 50)
    print(html_tags)

    # Generate optimization score
    score_data = generator._calculate_optimization_score(meta_tags)
    print(f"\nOptimization Score: {score_data['percentage']}%")
    print("\nFeedback:")
    for feedback in score_data['feedback']:
        print(f"  {feedback}")


if __name__ == "__main__":
    main()