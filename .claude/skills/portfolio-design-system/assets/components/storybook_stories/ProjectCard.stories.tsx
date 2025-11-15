import type { Meta, StoryObj } from '@storybook/react';
import { ProjectCard, Project } from '../react_components';

const sampleProject: Project = {
  id: '1',
  title: 'Portfolio Website',
  description: 'A modern, responsive portfolio website built with Next.js, TypeScript, and Tailwind CSS. Features smooth animations, dark mode support, and optimized performance.',
  image: 'https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=600&h=400&fit=crop',
  imageAlt: 'Portfolio website screenshot showing a clean, modern interface',
  technologies: [
    { name: 'Next.js', color: '#3178c6' },
    { name: 'TypeScript', color: '#3178c6' },
    { name: 'Tailwind CSS', color: '#06b6d4' },
    { name: 'React', color: '#61dafb' }
  ],
  liveUrl: 'https://example.com',
  githubUrl: 'https://github.com/example/portfolio',
  featured: true,
  status: 'completed'
};

const sampleProjectInProgress: Project = {
  id: '2',
  title: 'Task Management App',
  description: 'A collaborative task management application with real-time updates, drag-and-drop functionality, and team collaboration features.',
  image: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=400&fit=crop',
  imageAlt: 'Task management app interface with board layout',
  technologies: [
    { name: 'React', color: '#61dafb' },
    { name: 'Node.js', color: '#339933' },
    { name: 'MongoDB', color: '#47a248' },
    { name: 'Socket.io', color: '#010101' }
  ],
  githubUrl: 'https://github.com/example/tasks',
  status: 'in-progress'
};

const meta: Meta<typeof ProjectCard> = {
  title: 'Components/ProjectCard',
  component: ProjectCard,
  parameters: {
    layout: 'centered',
    tags: ['autodocs'],
    docs: {
      description: {
        component: 'Project showcase card component with technology tags, status indicators, and action links. Optimized for developer portfolios with clean, professional design.'
      }
    },
    a11y: {
      config: {
        rules: [
          { id: 'image-alt', enabled: true },
          { id: 'link-name', enabled: true },
          { id: 'color-contrast', enabled: true }
        ]
      }
    }
  },
  argTypes: {
    project: {
      control: 'object',
      description: 'Project data object'
    },
    variant: {
      control: 'select',
      options: ['default', 'compact', 'featured'],
      description: 'Visual variant of the project card'
    },
    showTags: {
      control: 'boolean',
      description: 'Whether to show technology tags'
    },
    showLinks: {
      control: 'boolean',
      description: 'Whether to show action links'
    },
    onClick: { action: 'clicked' }
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

// Default card
export const Default: Story = {
  args: {
    project: sampleProject,
    variant: 'default',
    showTags: true,
    showLinks: true
  }
};

// Compact variant
export const Compact: Story = {
  args: {
    project: sampleProjectInProgress,
    variant: 'compact',
    showTags: true,
    showLinks: false
  }
};

// Featured variant
export const Featured: Story = {
  args: {
    project: sampleProject,
    variant: 'featured',
    showTags: true,
    showLinks: true
  }
};

// Without image
export const WithoutImage: Story = {
  args: {
    project: {
      ...sampleProject,
      image: '',
      imageAlt: ''
    },
    variant: 'default',
    showTags: true,
    showLinks: true
  }
};

// In-progress project
export const InProgress: Story = {
  args: {
    project: sampleProjectInProgress,
    variant: 'default',
    showTags: true,
    showLinks: true
  }
};

// Without links
export const WithoutLinks: Story = {
  args: {
    project: sampleProject,
    variant: 'default',
    showTags: true,
    showLinks: false
  }
};

// Grid layout
export const GridLayout: Story = {
  render: () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl">
      <ProjectCard project={sampleProject} variant="default" />
      <ProjectCard project={sampleProjectInProgress} variant="compact" />
      <ProjectCard project={sampleProject} variant="featured" />
    </div>
  ),
  parameters: {
    viewport: {
      defaultViewport: 'responsive'
    }
  }
};

// Clickable cards
export const ClickableCards: Story = {
  render: () => {
    const handleCardClick = (project: Project) => {
      alert(`Clicked on ${project.title}`);
    };

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl">
        <ProjectCard
          project={sampleProject}
          onClick={handleCardClick}
          showLinks={false}
        />
        <ProjectCard
          project={sampleProjectInProgress}
          onClick={handleCardClick}
          showLinks={false}
        />
      </div>
    );
  }
};

// Different statuses
export const DifferentStatuses: Story = {
  render: () => {
    const projects: Project[] = [
      {
        ...sampleProject,
        id: '1',
        status: 'completed'
      },
      {
        ...sampleProject,
        id: '2',
        status: 'in-progress'
      },
      {
        ...sampleProject,
        id: '3',
        status: 'prototype'
      }
    ];

    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl">
        {projects.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            variant="compact"
          />
        ))}
      </div>
    );
  }
};

// Playground
export const Playground: Story = {
  args: {
    project: sampleProject,
    variant: 'default',
    showTags: true,
    showLinks: true
  }
};