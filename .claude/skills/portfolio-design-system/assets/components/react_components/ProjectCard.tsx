import React from 'react';

export interface Tech {
  name: string;
  color?: string;
  icon?: React.ReactNode;
}

export interface Project {
  id: string;
  title: string;
  description: string;
  image: string;
  imageAlt: string;
  technologies: Tech[];
  liveUrl?: string;
  githubUrl?: string;
  featured?: boolean;
  status?: 'completed' | 'in-progress' | 'prototype';
}

export interface ProjectCardProps {
  project: Project;
  variant?: 'default' | 'compact' | 'featured';
  showTags?: boolean;
  showLinks?: boolean;
  onClick?: (project: Project) => void;
  className?: string;
  'data-testid'?: string;
}

/**
 * Card component specifically for project showcases with technology tags and action links
 * @component
 */
export const ProjectCard: React.FC<ProjectCardProps> = ({
  project,
  variant = 'default',
  showTags = true,
  showLinks = true,
  onClick,
  className = '',
  'data-testid': testId
}) => {
  const cardClass = ProjectCardClassNames({ variant, className, hasImage: !!project.image });

  const handleCardClick = () => {
    onClick?.(project);
  };

  return (
    <article
      className={cardClass}
      onClick={handleCardClick}
      data-testid={testId || 'project-card'}
      role="article"
      aria-label={`Project: ${project.title}`}
    >
      {variant === 'featured' && project.featured && (
        <div className="project-card-badge">
          <span className="sr-only">Featured project</span>
          ⭐ Featured
        </div>
      )}

      {project.image && (
        <div className="project-card-image-container">
          <img
            src={project.image}
            alt={project.imageAlt}
            className="project-card-image"
            loading="lazy"
          />
          {project.status && (
            <div className="project-card-status">
              <span className="project-card-status-text">
                {project.status.replace('-', ' ')}
              </span>
            </div>
          )}
        </div>
      )}

      <div className="project-card-content">
        <header className="project-card-header">
          <h3 className="project-card-title">{project.title}</h3>
        </header>

        <p className="project-card-description">
          {project.description}
        </p>

        {showTags && project.technologies.length > 0 && (
          <div className="project-card-tags" aria-label="Technologies used">
            {project.technologies.map((tech, index) => (
              <span
                key={`${tech.name}-${index}`}
                className="project-card-tag"
                style={{ backgroundColor: tech.color ? `${tech.color}20` : undefined }}
              >
                {tech.icon && <span className="project-card-tag-icon">{tech.icon}</span>}
                {tech.name}
              </span>
            ))}
          </div>
        )}

        {showLinks && (project.liveUrl || project.githubUrl) && (
          <footer className="project-card-actions">
            {project.liveUrl && (
              <a
                href={project.liveUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="project-card-link project-card-link--primary"
                aria-label={`View live demo of ${project.title}`}
                onClick={(e) => e.stopPropagation()}
              >
                <span aria-hidden="true">🚀</span>
                Live Demo
              </a>
            )}
            {project.githubUrl && (
              <a
                href={project.githubUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="project-card-link project-card-link--secondary"
                aria-label={`View source code of ${project.title} on GitHub`}
                onClick={(e) => e.stopPropagation()}
              >
                <span aria-hidden="true">💻</span>
                Source Code
              </a>
            )}
          </footer>
        )}
      </div>
    </article>
  );
};

// Helper function for CSS classes
const ProjectCardClassNames = ({
  variant,
  className,
  hasImage
}: {
  variant: string;
  className: string;
  hasImage: boolean;
}) => {
  const baseClasses = [
    'project-card',
    'bg-white',
    'dark:bg-neutral-800',
    'rounded-xl',
    'shadow-md',
    'dark:shadow-lg',
    'border',
    'border-neutral-200',
    'dark:border-neutral-700',
    'overflow-hidden',
    'transition-all',
    'duration-300',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-primary-500',
    'focus:ring-offset-2'
  ];

  const variantClasses = {
    default: [
      'hover:shadow-xl',
      'hover:-translate-y-1',
      'cursor-pointer'
    ],
    compact: [
      'hover:shadow-lg',
      'hover:scale-105',
      'cursor-pointer'
    ],
    featured: [
      'ring-2',
      'ring-primary-500',
      'ring-offset-2',
      'dark:ring-offset-neutral-900',
      'hover:shadow-2xl',
      'hover:-translate-y-2',
      'cursor-pointer',
      'relative'
    ]
  };

  const layoutClasses = hasImage
    ? ['flex', 'flex-col']
    : ['flex', 'flex-col'];

  return [
    ...baseClasses,
    ...variantClasses[variant],
    ...layoutClasses,
    className
  ].filter(Boolean).join(' ');
};