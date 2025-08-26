import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Sidebar configuration for Slurm Factory Spack Repository documentation.
 */
const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'index',
      label: 'Getting Started',
    },
    {
      type: 'doc',
      id: 'getting-started',
      label: 'Quick Start',
    },
    {
      type: 'category',
      label: 'Packages',
      items: [
        'packages/slurm',
        'packages/curl',
        'packages/freeipmi',
        'packages/openssl',
      ],
    },
    {
      type: 'doc',
      id: 'contributing',
      label: 'Contributing',
    },
    {
      type: 'doc',
      id: 'contact',
      label: 'Contact',
    },
  ],
};

export default sidebars;
