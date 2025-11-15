import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '../react_components';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    tags: ['autodocs'],
    docs: {
      description: {
        component: 'Interactive button component with multiple variants, sizes, and accessibility features. Supports loading states, icons, and full-width layouts.'
      }
    },
    a11y: {
      config: {
        rules: [
          { id: 'button-name', enabled: true },
          { id: 'color-contrast', enabled: true }
        ]
      }
    }
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost'],
      description: 'Visual style variant of the button'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Size of the button'
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the button is disabled'
    },
    loading: {
      control: 'boolean',
      description: 'Whether the button is in loading state'
    },
    icon: {
      control: 'text',
      description: 'Icon to display (emoji or text)'
    },
    iconPosition: {
      control: 'select',
      options: ['left', 'right'],
      description: 'Position of the icon relative to text'
    },
    fullWidth: {
      control: 'boolean',
      description: 'Whether the button takes full width'
    },
    onClick: { action: 'clicked' },
    children: {
      control: 'text',
      description: 'Button content'
    }
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

// Default button
export const Default: Story = {
  args: {
    children: 'Click me',
    variant: 'primary',
    size: 'md'
  }
};

// All variants
export const Variants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4 items-center">
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  )
};

// All sizes
export const Sizes: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4 items-center">
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  )
};

// With icons
export const WithIcons: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4 items-center">
      <Button icon="🚀">Get Started</Button>
      <Button icon="⬅️" iconPosition="left" variant="outline">Back</Button>
      <Button icon="➡️" iconPosition="right" variant="secondary">Next</Button>
    </div>
  )
};

// Loading state
export const Loading: Story = {
  args: {
    children: 'Loading...',
    loading: true
  }
};

// Disabled state
export const Disabled: Story = {
  args: {
    children: 'Disabled',
    disabled: true
  }
};

// Full width
export const FullWidth: Story = {
  args: {
    children: 'Full Width Button',
    fullWidth: true
  },
  parameters: {
    viewport: {
      defaultViewport: 'mobile1'
    }
  }
};

// Interactive example
export const Interactive: Story = {
  render: () => {
    const [count, setCount] = React.useState(0);

    return (
      <div className="space-y-4">
        <Button onClick={() => setCount(count + 1)}>
          Clicked {count} times
        </Button>
        <Button
          variant="outline"
          onClick={() => setCount(0)}
          disabled={count === 0}
        >
          Reset
        </Button>
      </div>
    );
  }
};

// Accessibility testing example
export const AccessibilityExample: Story = {
  args: {
    children: 'Accessible Button',
    'aria-label': 'Perform primary action',
    'aria-describedby': 'button-description'
  },
  render: (args) => (
    <div>
      <Button {...args} />
      <p id="button-description" className="sr-only">
        This button performs the primary action on the page
      </p>
    </div>
  )
};

// Playground
export const Playground: Story = {
  args: {
    children: 'Play with me!',
    variant: 'primary',
    size: 'md',
    disabled: false,
    loading: false,
    icon: '',
    iconPosition: 'left',
    fullWidth: false
  }
};