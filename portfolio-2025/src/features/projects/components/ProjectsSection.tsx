'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/shared/components/ui/Button'
import { githubAPI, type GitHubRepo } from '@/shared/lib/github'
import { Card } from '@/shared/components/ui/Card'

interface ProjectCardProps {
  repo: GitHubRepo
  index: number
}

function ProjectCard({ repo, index }: ProjectCardProps) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.6 }}
      whileHover={{ y: -10, scale: 1.02 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
    >
      <Card className="h-full glass-dark border-primary-500/20 hover:border-primary-500/50 transition-all duration-300 overflow-hidden group">
        {/* Gradient overlay on hover */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-600/10 via-transparent to-secondary-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

        <div className="p-6 relative z-10">
          {/* Header with language color */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-gradient-to-r from-green-400 to-blue-500 animate-pulse" />
              <h3 className="text-xl font-bold text-foreground group-hover:text-primary-400 transition-colors">
                {repo.name.replace(/[-_]/g, ' ').toUpperCase()}
              </h3>
            </div>
            {repo.language && (
              <span className="text-xs px-2 py-1 rounded-full bg-primary-500/20 text-primary-400 font-mono">
                {repo.language}
              </span>
            )}
          </div>

          {/* Description */}
          <p className="text-foreground/70 mb-6 line-clamp-3">
            {repo.description || 'An innovative project showcasing cutting-edge technology and creative solutions.'}
          </p>

          {/* Stats */}
          <div className="flex items-center gap-6 text-sm text-foreground/60 mb-6">
            <div className="flex items-center gap-2">
              <span className="text-yellow-400">⭐</span>
              <span>{repo.stargazers_count}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-blue-400">🍴</span>
              <span>{repo.forks_count}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-purple-400">👁️</span>
              <span>{repo.watchers_count}</span>
            </div>
          </div>

          {/* Technologies */}
          {repo.topics && repo.topics.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-6">
              {repo.topics.slice(0, 3).map((topic) => (
                <span
                  key={topic}
                  className="text-xs px-2 py-1 rounded-full bg-gradient-to-r from-primary-500/20 to-secondary-500/20 text-foreground/70 border border-primary-500/30"
                >
                  {topic}
                </span>
              ))}
            </div>
          )}

          {/* Action buttons */}
          <div className="flex gap-3">
            <Button
              size="sm"
              variant="outline"
              className="group/btn flex-1 border-primary-500/50 hover:border-primary-400 hover:bg-primary-500/10"
              onClick={() => window.open(repo.html_url, '_blank')}
            >
              <span className="flex items-center gap-2">
                <span className="text-lg">📁</span>
                <span>View Code</span>
              </span>
            </Button>

            {repo.homepage && (
              <Button
                size="sm"
                variant="gradient"
                className="group/btn flex-1"
                onClick={() => window.open(repo.homepage!, '_blank')}
              >
                <span className="flex items-center gap-2">
                  <span className="text-lg">🚀</span>
                  <span>Live Demo</span>
                </span>
              </Button>
            )}
          </div>
        </div>

        {/* Animated border effect */}
        <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-primary-600 via-secondary-500 to-accent-400 opacity-0 group-hover:opacity-20 transition-opacity duration-300 -z-10" />
      </Card>
    </motion.div>
  )
}

export function ProjectsSection() {
  const [repos, setRepos] = useState<GitHubRepo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadProjects = async () => {
      try {
        setLoading(true)
        // Using a popular GitHub username for demo - replace with actual username
        const featuredRepos = await githubAPI.getFeaturedRepos('vercel', 6)
        setRepos(featuredRepos)
      } catch (err) {
        console.error('Error loading projects:', err)
        setError('Failed to load projects')
        // Fallback demo data
        setRepos([
          {
            id: 1,
            name: 'ai-automation-platform',
            full_name: 'demo/ai-automation-platform',
            description: 'Intelligent automation platform powered by cutting-edge AI technologies for streamlining business workflows.',
            html_url: 'https://github.com',
            homepage: 'https://demo.com',
            language: 'TypeScript',
            stargazers_count: 1250,
            watchers_count: 89,
            forks_count: 340,
            open_issues_count: 12,
            topics: ['ai', 'automation', 'typescript', 'react'],
            visibility: 'public' as const,
            default_branch: 'main',
            size: 2500,
            archived: false,
            disabled: false,
            fork: false,
            license: null,
            owner: {
              login: 'demo',
              id: 1,
              avatar_url: '',
              html_url: '',
              type: 'User'
            },
            created_at: '2024-01-15',
            updated_at: '2024-11-14',
            pushed_at: '2024-11-14'
          },
          {
            id: 2,
            name: 'neural-chat-system',
            full_name: 'demo/neural-chat-system',
            description: 'Advanced conversational AI system with natural language processing and real-time response capabilities.',
            html_url: 'https://github.com',
            homepage: null,
            language: 'Python',
            stargazers_count: 890,
            watchers_count: 67,
            forks_count: 210,
            open_issues_count: 8,
            topics: ['python', 'ai', 'nlp', 'machine-learning'],
            visibility: 'public' as const,
            default_branch: 'main',
            size: 1800,
            archived: false,
            disabled: false,
            fork: false,
            license: null,
            owner: {
              login: 'demo',
              id: 1,
              avatar_url: '',
              html_url: '',
              type: 'User'
            },
            created_at: '2024-02-20',
            updated_at: '2024-11-10',
            pushed_at: '2024-11-10'
          }
        ])
      } finally {
        setLoading(false)
      }
    }

    loadProjects()
  }, [])

  return (
    <section id="projects" className="min-h-screen bg-gradient-to-br from-background via-secondary-50/5 to-background py-20">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="gradient-text bg-gradient-to-r from-primary-600 via-secondary-500 to-accent-400 bg-clip-text text-transparent">
              Featured Projects
            </span>
          </h2>
          <p className="text-xl text-foreground/70 max-w-3xl mx-auto">
            Explore my latest innovations in AI, automation, and cutting-edge web development.
            Each project represents a unique solution to complex technical challenges.
          </p>
        </motion.div>

        {/* Loading State */}
        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-64 bg-foreground/10 rounded-lg border border-foreground/20">
                  <div className="p-6">
                    <div className="h-4 bg-foreground/20 rounded mb-4 w-3/4" />
                    <div className="h-3 bg-foreground/15 rounded mb-2" />
                    <div className="h-3 bg-foreground/15 rounded mb-6 w-5/6" />
                    <div className="flex gap-2 mb-4">
                      <div className="h-6 bg-foreground/15 rounded-full w-16" />
                      <div className="h-6 bg-foreground/15 rounded-full w-20" />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Projects Grid */}
        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {repos.map((repo, index) => (
              <ProjectCard key={repo.id} repo={repo} index={index} />
            ))}
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">⚠️</div>
            <h3 className="text-2xl font-bold mb-2">Oops! Something went wrong</h3>
            <p className="text-foreground/70 mb-6">Unable to load projects at the moment.</p>
            <Button onClick={() => window.location.reload()}>
              Try Again
            </Button>
          </div>
        )}

        {/* Call to Action */}
        <motion.div
          className="text-center mt-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Button
            size="lg"
            variant="outline"
            className="border-2 border-primary-500/50 hover:border-primary-400 hover:bg-primary-500/10"
            onClick={() => window.open('https://github.com', '_blank')}
          >
            View All Projects on GitHub
          </Button>
        </motion.div>
      </div>
    </section>
  )
}