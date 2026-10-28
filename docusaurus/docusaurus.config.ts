// Copyright 2025 Vantage Compute Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import * as fs from 'fs';
import * as path from 'path';
import type {Config} from '@docusaurus/types';
import {staticDir, getProjectVersion, vantagePrism} from '@vantagecompute/docusaurus-theme';

// From the theme rather than read out of pyproject.toml, so every Vantage site
// advertises its version the same way. It returns `git describe --tags
// --always`, so the string already carries its leading `v`. A docs-only release
// is tagged docs-vX.Y.Z; the site shows the version, not the tag.
const projectVersion = getProjectVersion().replace(/^docs-/, '');

const projectRoot = path.join(__dirname, '..');

// The package reference is generated at build time by
// @vantagecompute/docusaurus-plugin-pydoc from the Spack package recipes. It
// parses each package.py with `ast` and never imports it, which is the only way
// to document a recipe: importing one needs a Spack installation
// (`from spack.package import *`).
//
// The package list is read from the repository so a new package cannot be
// forgotten. Each package is a directory holding a package.py; the module name
// mirrors that path, and the label is the directory name.
const packagesDir = path.join(projectRoot, 'spack_repo', 'slurm_factory', 'packages');

const pydocModules = fs
  .readdirSync(packagesDir, {withFileTypes: true})
  .filter((entry) => entry.isDirectory() && fs.existsSync(path.join(packagesDir, entry.name, 'package.py')))
  .map((entry) => entry.name)
  .sort()
  .map((name) => ({module: `spack_repo.slurm_factory.packages.${name}.package`, label: name}));

const config: Config = {
  title: 'Slurm Factory Spack Repo',
  tagline: `Custom Spack repository for building and installing Slurm (${projectVersion})`,
  favicon: 'img/favicon.ico',

  // A spoke site under the docs hub. Authentication happens at the edge: the
  // Lambda@Edge Keycloak gateway guards all of /developer/*, so this site
  // carries no login of its own. `noIndex` because the hub is not public.
  url: 'https://docs.vantagecompute.ai',
  baseUrl: '/developer/slurm-factory-spack-repo/',
  noIndex: true,

  // Published only to the vantage-docs hub, by deploy-docs.yml (S3 + CloudFront). No
  // organizationName/projectName: those configure `docusaurus deploy`, which pushes to GitHub
  // Pages, and this site never goes there.
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  markdown: {
    format: 'detect',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },
  // The theme renders the navbar and (no) footer itself: this site is a
  // developer spoke, so it gets the developer navbar with the brand mark, the
  // centred title and version, and these buttons. There is no
  // themeConfig.navbar and no footer below; both belong to the theme.
  // The Vantage theme comes after theme-mermaid so its Mermaid override (the Vantage
  // palette and type) takes effect.
  themes: [
    '@docusaurus/theme-mermaid',
    [
      '@vantagecompute/docusaurus-theme',
      {
        navbarLinks: [
          {label: 'GitHub', url: 'https://github.com/vantagecompute/slurm-factory-spack-repo'},
          {label: 'Buildcache', url: 'https://slurm-factory-spack-binary-cache.vantagecompute.ai'},
        ],
      },
    ],
  ],

  staticDirectories: [staticDir],

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
      },
    ],
  ],
  plugins: [
    [
      '@vantagecompute/docusaurus-plugin-pydoc',
      {
        projectRoot,
        modules: pydocModules,
        outputDir: './docs/package-reference',
        label: 'Package Reference',
        python: process.env.PYDOC_PYTHON ?? 'python3',
      },
    ],
    [
      'docusaurus-plugin-llms',
      {
        generateLLMsTxt: true,
        generateLLMsFullTxt: true,
        docsDir: 'docs',
        title: 'Slurm Factory Spack Repository Documentation',
        description:
          'Custom Spack repository for building and installing Slurm with pre-built binaries and GPU support.',
        includeBlog: false,
        excludeImports: true,
        removeDuplicateHeadings: true,
        generateMarkdownFiles: true,
        includeOrder: [],
        includeUnmatchedLast: true,
        pathTransformation: {
          ignorePaths: ['docs'],
        },
        customLLMFiles: [
          {
            filename: 'llms-getting-started.txt',
            includePatterns: ['docs/index.md', 'docs/getting-started.md'],
            fullContent: true,
            title: 'Slurm Factory Spack Repository Getting Started',
            description: 'Overview, installation and quick start for the Slurm Factory Spack repository',
          },
          {
            filename: 'llms-packages.txt',
            includePatterns: ['docs/packages/*.md'],
            fullContent: true,
            title: 'Slurm Factory Package Documentation',
            description: 'Guides for the slurm, curl, freeipmi, openssl and s2n-tls packages',
          },
          {
            filename: 'llms-package-reference.txt',
            includePatterns: ['docs/package-reference/**/*.md'],
            fullContent: true,
            title: 'Slurm Factory Package Reference',
            description: 'Package recipe reference generated from the Spack package.py docstrings',
          },
          {
            filename: 'llms-project.txt',
            includePatterns: ['docs/contributing.md', 'docs/releasing.md', 'docs/contact.md'],
            fullContent: true,
            title: 'Slurm Factory Spack Repository Project Guide',
            description: 'Contributing, releasing and contact information',
          },
        ],
      },
    ],
  ],

  customFields: {
    projectVersion: projectVersion,
  },

  themeConfig: {
    codeBlock: {
      showCopyButton: true,
    },
    // The Vantage light and dark code themes and the grammars every Vantage site needs,
    // plus Dockerfile highlighting for the build pages.
    prism: {
      ...vantagePrism,
      additionalLanguages: [...vantagePrism.additionalLanguages, 'docker'],
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 5,
    },
  },
};

export default config;
