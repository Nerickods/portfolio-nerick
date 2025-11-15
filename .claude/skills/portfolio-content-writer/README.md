# Portfolio Content Writer Skill

A specialized skill for generating professional portfolio content including project descriptions, about sections, blog posts, and contact templates. Transforms technical achievements into compelling business value narratives that attract opportunities.

## 🎯 Purpose

This skill helps developers create professional, SEO-optimized portfolio content that:
- **Converts technical features into business value**
- **Quantifies impact with specific metrics**
- **Showcases expertise through compelling narratives**
- **Optimizes content for search visibility**
- **Maintains professional yet authentic tone**

## 🚀 Quick Start

### Installation
1. Copy this skill to your `.claude/skills/` directory
2. Ensure Python 3.8+ is installed
3. Install dependencies if needed

### Basic Usage

```bash
# Analyze your project
python scripts/content_generator.py analyze --project-path ./your-project --output project_analysis.json

# Generate project description
python scripts/content_generator.py project-description --project-path ./your-project --output project_description.md

# Create about section
python scripts/template_engine.py generate --template about_me --style technical --output about_me.md

# Generate blog post
python scripts/content_generator.py blog-post --project-path ./your-project --style tutorial --output blog_post.md

# Create impact analysis
python scripts/impact_analyzer.py --project-metrics ./project_analysis.json --output impact_report.md
```

## 📁 Skill Structure

```
portfolio-content-writer/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── scripts/                    # Content generation tools
│   ├── content_generator.py    # Main content analysis and generation
│   ├── template_engine.py      # Template processing and customization
│   └── impact_analyzer.py      # Impact metrics and business value analysis
├── references/                 # Documentation and guidelines
│   ├── writing_patterns.md     # Proven writing structures and patterns
│   ├── seo_guidelines.md       # SEO optimization guidelines
│   └── tone_examples.md        # Tone and style examples
└── assets/                     # Templates and examples
    ├── templates/               # Content templates
    │   ├── project_description.md
    │   ├── about_me.md
    │   ├── blog_post.md
    │   └── contact_email.md
    └── examples/                # Sample generated content
        └── sample_project_description.md
```

## 🛠️ Core Scripts

### content_generator.py
Main script for analyzing projects and generating content.

**Features:**
- Automatic project analysis from codebase
- README and commit history parsing
- Technology stack extraction
- Feature identification and categorization
- Multiple content type generation

**Usage:**
```bash
python scripts/content_generator.py analyze --project-path ./your-project --output analysis.json
python scripts/content_generator.py project-description --project-path ./your-project --output description.md
python scripts/content_generator.py about-section --project-path ./your-project --output about.md
python scripts/content_generator.py blog-post --project-path ./your-project --style tutorial --output blog.md
```

### template_engine.py
Template processing system for consistent content generation.

**Features:**
- Multiple content templates (about, contact, project summaries)
- Customizable styles (technical, business, casual)
- Template creation and customization
- Context-aware content generation

**Usage:**
```bash
python scripts/template_engine.py generate --template about_me --style technical --output about.md
python scripts/template_engine.py generate --template contact_email --purpose job_application --company "Acme Corp" --output email.md
python scripts/template_engine.py create-template --name custom --fields "field1,field2,field3" --output custom_template.md
```

### impact_analyzer.py
Analyzes project impact and generates quantifiable metrics.

**Features:**
- Performance impact estimation
- Business value calculation
- User impact analysis
- Technical achievement assessment
- Innovation scoring

**Usage:**
```bash
python scripts/impact_analyzer.py --project-metrics ./project_data.json --output impact_report.json
python scripts/impact_analyzer.py --project-metrics ./project_data.json --format markdown --output impact_report.md
```

## 📝 Content Types

### Project Descriptions
Transform technical implementation into compelling business narratives:
- Problem-solution-outcome structure
- Quantified impact metrics
- Technical architecture overview
- Live demo and source links

### About Sections
Professional biographies with multiple tones:
- **Technical**: Focus on skills and architecture
- **Business**: Emphasis on impact and leadership
- **Casual**: Personality and culture fit
- **Leadership**: Team building and strategic vision

### Blog Posts
Educational content showcasing expertise:
- **Tutorial**: Step-by-step technical guides
- **Case Study**: Detailed project analysis
- **Lessons Learned**: Reflections and insights
- **Future Predictions**: Industry trends and opinions

### Contact Templates
Professional outreach messages:
- **Job Applications**: Tailored cover letters and introductions
- **Freelance Proposals**: Project proposals and scope definitions
- **Networking**: Professional relationship building
- **Follow-ups**: Professional persistence and follow-through

## 🎨 Tone and Style

### Professional Standards
- **Results-Oriented**: Focus on measurable impact
- **Business Value**: Translate technical features to business benefits
- **SEO Optimized**: Proper structure and keyword integration
- **Authentic Voice**: Maintain genuine personality while professional

### Tone Variations
- **Technical Expert**: Precise, confident, architecture-focused
- **Business Leader**: Strategic, ROI-focused, market-aware
- **Approachable Authentic**: Personal, relatable, humble yet confident
- **Innovation-Driven**: Forward-thinking, visionary, ambitious

## 📊 Impact Metrics

### Performance Metrics
- Load time improvements (e.g., "60% faster page loads")
- Database optimization (e.g., "90% query time reduction")
- Cache hit rates (e.g., "85% cache hit rate")
- Scalability achievements (e.g., "10K concurrent users")

### Business Metrics
- Revenue impact (e.g., "$120K monthly recurring revenue")
- Cost savings (e.g., "40% reduction in infrastructure costs")
- User engagement (e.g., "35% improvement in user retention")
- Conversion rates (e.g., "25% increase in conversion rate")

### Technical Achievements
- System reliability (e.g., "99.99% uptime")
- Code quality (e.g., "90% test coverage")
- Deployment efficiency (e.g., "75% reduction in deployment time")
- Security improvements (e.g., "100% vulnerability remediation")

## 🔧 Integration Examples

### Next.js 16 Integration
```typescript
// app/portfolio/page.tsx
import { cache } from 'react';

async function getPortfolioContent() {
  'use cache';

  // Use generated content from portfolio-content-writer
  const content = await import('../../generated/portfolio-content.json');
  return content.default;
}

export default async function PortfolioPage() {
  const content = await getPortfolioContent();

  return (
    <div>
      <AboutSection content={content.about} />
      <ProjectsList projects={content.projects} />
      <BlogPosts posts={content.blogPosts} />
    </div>
  );
}
```

### Supabase Integration
```typescript
// lib/portfolio-content.ts
import { supabase } from './supabase';

export async function savePortfolioContent(content: PortfolioContent) {
  const { data, error } = await supabase
    .from('portfolio_content')
    .upsert({
      id: content.id,
      project_descriptions: content.projects,
      about_section: content.about,
      blog_posts: content.posts,
      updated_at: new Date().toISOString(),
    });

  return { data, error };
}
```

## 📚 Best Practices

### DO ✅
- **Quantify Everything**: Use specific numbers and percentages
- **Focus on Impact**: Business value over technical features
- **Tell Stories**: Create narrative around problem-solving
- **Be Authentic**: Use your actual experience and voice
- **Optimize for SEO**: Include keywords and proper structure
- **Update Regularly**: Keep content fresh with new achievements

### DON'T ❌
- **Use Generic Descriptions**: Make content specific to your experience
- **Forget Your Audience**: Tailor technical depth appropriately
- **Overlook SEO**: Optimize for search discoverability
- **Skip Proofreading**: Ensure professional polish
- **Be Overly Technical**: Translate jargon to business value
- **Forget Call-to-Action**: Guide visitors to next steps

## 🎯 Content Quality Checklist

### Project Description Validation
- [ ] Clear problem statement with business context
- [ ] Specific solutions with technical approach
- [ ] Measurable results with concrete numbers
- [ ] Technology stack relevant to target role
- [ ] Live demo link for verification
- [ ] Source code available for review
- [ ] SEO optimized for search visibility

### About Section Validation
- [ ] Professional headline with expertise areas
- [ ] Technical skills categorized by domain
- [ ] Key achievements with impact metrics
- [ ] Career narrative showing growth
- [ ] Personal brand consistency
- [ ] Contact information easily accessible
- [ ] Call-to-action for next steps

### Email Template Validation
- [ ] Clear subject line and purpose
- [ ] Personalized to recipient
- [ ] Value proposition clearly stated
- [ ] Relevant experience highlighted
- [ ] Specific call-to-action included
- [ ] Professional contact information
- [ ] Appropriate tone for context

## 🔍 SEO Guidelines

### Keyword Strategy
- **Primary Keywords**: Role + technology combinations
- **Secondary Keywords**: Industry-specific terms and problems
- **Long-Tail Keywords**: Specific project types and achievements

### Content Structure
- **H1**: Main title with primary keyword
- **H2**: Major sections with secondary keywords
- **H3**: Subsections with related keywords
- **Meta Descriptions**: Under 160 characters with value proposition

### Technical SEO
- Proper heading hierarchy
- Image alt text with keywords
- Internal linking between content
- Mobile-responsive formatting
- Fast loading optimization

## 🚀 Advanced Features

### Custom Templates
```python
# Create custom template for your specific needs
python scripts/template_engine.py create-template \
  --name "tech_startup_project" \
  --fields "problem,solution,traction,team,tech_stack,funding" \
  --output custom_template.md
```

### Batch Processing
```bash
# Process multiple projects at once
for project in projects/*; do
  python scripts/content_generator.py project-description \
    --project-path "$project" \
    --output "content/$(basename "$project")_description.md"
done
```

### Content Optimization
```python
# Optimize existing content for SEO
python scripts/seo_optimizer.py \
  --content ./existing_content.md \
  --keywords "full-stack developer,react,node.js" \
  --target-audience "hiring-managers" \
  --output optimized_content.md
```

## 🔗 Resources

### Writing Patterns
- **Problem-Solution-Outcome**: Classic storytelling structure
- **Feature-Benefit**: Connect technical features to user benefits
- **Before-After**: Show transformation and improvement
- **STAR Method**: Situation-Task-Action-Result for interviews

### Tone Examples
- **Technical Recruiter**: Focus on architecture and scalability
- **Business Stakeholder**: Emphasize ROI and business value
- **Fellow Developer**: Share technical insights and challenges
- **Startup Founder**: Show innovation and market understanding

### SEO Best Practices
- **Content Quality**: Comprehensive, valuable, and unique
- **Keyword Research**: Target relevant search terms
- **Technical Optimization**: Speed, mobile, and structure
- **User Experience**: Clear navigation and engagement

## 🤝 Contributing

This skill is designed to be extensible. To contribute:

1. **Add Templates**: Create new content templates in `assets/templates/`
2. **Improve Analysis**: Enhance pattern recognition in scripts
3. **Update Guidelines**: Add new writing patterns and tone examples
4. **Fix Issues**: Report and fix bugs in content generation

## 📄 License

MIT License - feel free to use, modify, and distribute for personal and commercial projects.

---

**Portfolio Content Writer** transforms your technical achievements into compelling professional narratives that attract opportunities and showcase your expertise effectively.

*Generate professional portfolio content that converts visitors into opportunities.*