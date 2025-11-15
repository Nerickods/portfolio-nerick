export interface GitHubRepo {
  id: number
  name: string
  full_name: string
  description: string | null
  html_url: string
  homepage: string | null
  language: string | null
  languages?: Record<string, number>
  stargazers_count: number
  watchers_count: number
  forks_count: number
  open_issues_count: number
  created_at: string
  updated_at: string
  pushed_at: string
  topics: string[]
  visibility: 'public' | 'private'
  default_branch: string
  size: number
  archived: boolean
  disabled: boolean
  fork: boolean
  license: {
    key: string
    name: string
    spdx_id: string
    url: string | null
    node_id: string
  } | null
  owner: {
    login: string
    id: number
    avatar_url: string
    html_url: string
    type: string
  }
}

export interface GitHubUser {
  login: string
  id: number
  avatar_url: string
  html_url: string
  name: string | null
  company: string | null
  blog: string | null
  location: string | null
  email: string | null
  bio: string | null
  twitter_username: string | null
  public_repos: number
  followers: number
  following: number
  created_at: string
  updated_at: string
}

class GitHubAPI {
  private baseURL = 'https://api.github.com'
  private token: string | null = null
  private cache = new Map<string, { data: any; timestamp: number }>()
  private cacheDuration = 15 * 60 * 1000 // 15 minutes

  constructor() {
    // Only set token on server side
    if (typeof window === 'undefined') {
      this.token = process.env.GITHUB_TOKEN || null
    }
  }

  private isCacheValid(key: string): boolean {
    const cached = this.cache.get(key)
    if (!cached) return false

    return Date.now() - cached.timestamp < this.cacheDuration
  }

  private setCache(key: string, data: any): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    })
  }

  private getCache(key: string): any | null {
    const cached = this.cache.get(key)
    if (!cached || !this.isCacheValid(key)) {
      this.cache.delete(key)
      return null
    }

    return cached.data
  }

  private async fetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const cacheKey = `${endpoint}:${JSON.stringify(options)}`

    // Try cache first for GET requests
    if (!options.method || options.method === 'GET') {
      const cached = this.getCache(cacheKey)
      if (cached) return cached
    }

    const url = `${this.baseURL}${endpoint}`
    const headers: Record<string, string> = {
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'Portfolio-2025/1.0.0',
      ...(options.headers as Record<string, string> || {}),
    }

    if (this.token) {
      headers['Authorization'] = `token ${this.token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()

      // Cache GET requests
      if (!options.method || options.method === 'GET') {
        this.setCache(cacheKey, data)
      }

      return data
    } catch (error) {
      console.error('GitHub API error:', error)
      throw error
    }
  }

  async getUser(username: string): Promise<GitHubUser> {
    return this.fetch<GitHubUser>(`/users/${username}`)
  }

  async getRepos(username: string, options: {
    type?: 'all' | 'owner' | 'member'
    sort?: 'created' | 'updated' | 'pushed' | 'full_name'
    direction?: 'asc' | 'desc'
    per_page?: number
    page?: number
  } = {}): Promise<GitHubRepo[]> {
    const params = new URLSearchParams({
      type: options.type || 'owner',
      sort: options.sort || 'updated',
      direction: options.direction || 'desc',
      per_page: String(options.per_page || 100),
      page: String(options.page || 1),
    })

    return this.fetch<GitHubRepo[]>(`/users/${username}/repos?${params}`)
  }

  async getRepoLanguages(owner: string, repo: string): Promise<Record<string, number>> {
    return this.fetch<Record<string, number>>(`/repos/${owner}/${repo}/languages`)
  }

  async getFeaturedRepos(username: string, maxRepos: number = 6): Promise<GitHubRepo[]> {
    try {
      const repos = await this.getRepos(username, {
        sort: 'updated',
        per_page: maxRepos * 2, // Get more to filter
      })

      // Filter out forks and archived repos, then limit
      const filtered = repos
        .filter(repo => !repo.fork && !repo.archived && repo.description)
        .slice(0, maxRepos)

      // Enrich with language details
      const enriched = await Promise.all(
        filtered.map(async (repo) => {
          try {
            const languages = await this.getRepoLanguages(repo.owner.login, repo.name)
            return { ...repo, languages }
          } catch (error) {
            console.warn(`Failed to fetch languages for ${repo.name}:`, error)
            return { ...repo, languages: {} }
          }
        })
      )

      return enriched
    } catch (error) {
      console.error('Error fetching featured repos:', error)
      return []
    }
  }

  async getUserStats(username: string): Promise<{
    totalRepos: number
    totalStars: number
    totalForks: number
    languages: Array<{ name: string; count: number; percentage: number }>
  }> {
    try {
      const repos = await this.getRepos(username, {
        type: 'owner',
        per_page: 100
      })

      const totalRepos = repos.length
      const totalStars = repos.reduce((sum, repo) => sum + repo.stargazers_count, 0)
      const totalForks = repos.reduce((sum, repo) => sum + repo.forks_count, 0)

      // Calculate language distribution
      const languageMap = new Map<string, number>()

      for (const repo of repos) {
        if (repo.language && !repo.archived) {
          languageMap.set(
            repo.language,
            (languageMap.get(repo.language) || 0) + 1
          )
        }
      }

      const totalLanguageCount = Array.from(languageMap.values()).reduce((a, b) => a + b, 0)
      const languages = Array.from(languageMap.entries())
        .map(([name, count]) => ({
          name,
          count,
          percentage: Math.round((count / totalLanguageCount) * 100)
        }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 10) // Top 10 languages

      return {
        totalRepos,
        totalStars,
        totalForks,
        languages
      }
    } catch (error) {
      console.error('Error fetching user stats:', error)
      return {
        totalRepos: 0,
        totalStars: 0,
        totalForks: 0,
        languages: []
      }
    }
  }

  // Clear cache method for testing or manual refresh
  clearCache(): void {
    this.cache.clear()
  }
}

export const githubAPI = new GitHubAPI()