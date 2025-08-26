import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import * as fs from 'fs';
import * as path from 'path';

// Function to read version from pyproject.toml
function getVersionFromPyproject(): string {
  try {
    const pyprojectPath = path.join(__dirname, '../pyproject.toml');
    const content = fs.readFileSync(pyprojectPath, 'utf8');
    
    // Extract version using regex
    const versionMatch = content.match(/^version\s*=\s*["']([^"']+)["']/m);
    
    if (versionMatch) {
      return versionMatch[1];
    }
    
    throw new Error('Version not found in pyproject.toml');
  } catch (error) {
    console.error('Error reading version from pyproject.toml:', error);
    return '0.0.0'; // fallback version
  }
}

const projectVersion = getVersionFromPyproject();

const config: Config = {
  title: 'Slurm Factory Spack Repo',
  tagline: 'Custom Spack repository for building and installing Slurm',
  favicon: 'img/favicon.ico',

  url: 'https://vantagecompute.github.io',
  baseUrl: '/slurm-factory-spack-repo/',

  organizationName: 'vantagecompute',
  projectName: 'slurm-factory-spack-repo',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  markdown: {
    format: 'mdx',
    mermaid: false,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: './docs',
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/vantagecompute/slurm-factory-spack-repo/tree/main/docusaurus/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  plugins: [
    [
      'docusaurus-plugin-llms',
      {
        // Generate llms.txt files for AI consumption
        generateLLMsTxt: true,
        generateLLMsFullTxt: true,
        docsDir: 'docs',
        ignoreFiles: [],
        title: 'Slurm Factory Spack Repository Documentation',
        description: 'Custom Spack repository for building and installing Slurm with pre-built binaries and GPU support.',
        includeBlog: false,
        // Content cleaning options
        excludeImports: true,
        removeDuplicateHeadings: true,
        // Generate individual markdown files following llmstxt.org specification
        generateMarkdownFiles: true,
        // Control documentation order
        includeOrder: [],
        includeUnmatchedLast: true,
        // Path transformation options
        pathTransformation: {
          // Paths to ignore when constructing URLs (will be removed if found)
          ignorePaths: ['docs'],
        },
        // Custom LLM files for specific documentation sections
        customLLMFiles: [
          {
            filename: 'llms-index.txt',
            includePatterns: ['docs/index.md'],
            fullContent: true,
            title: 'Slurm Factory Spack Repository Overview',
            description: 'Overview and introduction to Slurm Factory Spack Repository'
          },
          {
            filename: 'llms-getting-started.txt',
            includePatterns: ['docs/getting-started.md'],
            fullContent: true,
            title: 'Slurm Factory Getting Started Guide',
            description: 'Installation and quick start guide for Slurm Factory'
          },
          {
            filename: 'llms-packages.txt',
            includePatterns: ['docs/packages/*.md'],
            fullContent: true,
            title: 'Slurm Factory Package Documentation',
            description: 'Complete package reference for Slurm, curl, freeipmi, and openssl'
          },
          {
            filename: 'llms-contributing.txt',
            includePatterns: ['docs/contributing.md'],
            fullContent: true,
            title: 'Slurm Factory Contributing Guide',
            description: 'Contributing guidelines for Slurm Factory Spack Repository'
          },
          {
            filename: 'llms-contact.txt',
            includePatterns: ['docs/contact.md'],
            fullContent: true,
            title: 'Slurm Factory Contact Information',
            description: 'Contact and support information for Slurm Factory'
          },
        ],
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Slurm Factory Spack Repo',
      logo: {
        alt: 'Vantage Compute Logo',
        src: 'https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-white-horz.png',
        srcDark: 'https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-white-horz.png',
        href: 'https://vantagecompute.github.io/slurm-factory-spack-repo/',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://github.com/vantagecompute/slurm-factory-spack-repo',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: '/',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/vantagecompute/slurm-factory-spack-repo',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Vantage Compute. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

export default config;
