# Slurm Factory Spack Repository docs

The documentation site, built with [Docusaurus](https://docusaurus.io/) on
`@vantagecompute/docusaurus-theme` and published as the `slurm-factory-spack-repo` spoke
under `/developer/slurm-factory-spack-repo/` on docs.vantagecompute.ai.

The Package Reference is generated on every build by
`@vantagecompute/docusaurus-plugin-pydoc` from the docstrings in
`spack_repo/slurm_factory/packages/*/package.py`. It parses the recipes and never imports
them, so no Spack installation is needed. The generated pages are gitignored; edit the
docstrings, not the pages.

```bash
just docs-dev     # development server
just docs-build   # production build into build/
just docs-serve   # serve the production build
```

`deploy-docs.yml` deploys the site on `vX.Y.Z` and `docs-vX.Y.Z` tags. See
`docs/releasing.md`.
