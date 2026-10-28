# Contributing

Thank you for your interest in contributing to the Slurm Factory Spack Repository! This guide will help you get started.

## Ways to Contribute

There are many ways to contribute:

- **Report bugs**: Help us identify and fix issues
- **Suggest features**: Propose new packages or variants
- **Improve documentation**: Fix typos, clarify instructions, add examples
- **Submit patches**: Fix bugs or add features
- **Test packages**: Verify builds on different platforms
- **Add packages**: Contribute new package definitions

## Getting Started

### Prerequisites

- Git and GitHub account
- Spack 1.0 or later installed locally
- [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/), for the repository checks
- Node.js and Yarn, if you build the docs
- Familiarity with Spack package development
- Basic understanding of Python

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR-USERNAME/slurm-factory-spack-repo.git
cd slurm-factory-spack-repo
```

3. Add the upstream remote:

```bash
git remote add upstream https://github.com/vantagecompute/slurm-factory-spack-repo.git
```

## Development Workflow

### 1. Create a Branch

Create a descriptive branch for your changes:

```bash
git checkout -b fix/slurm-s2n-rpath
# or
git checkout -b feature/add-new-package
# or
git checkout -b docs/update-getting-started
```

### 2. Make Changes

Edit the package files in `spack_repo/slurm_factory/packages/`. Each package lives in its own directory as `package.py`; directory names must be valid Python module names, so a package such as `s2n-tls` lives in `s2n_tls/`.

### 3. Test Your Changes

Add the repository and test your changes:

```bash
# Add your local repository
spack repo add $(pwd)/spack_repo/slurm_factory

# Check the package concretizes
spack spec slurm_factory.slurm@26-05-5-1 +your-new-variant

# Test actual build (if needed)
spack install --test=root slurm_factory.slurm@26-05-5-1 +your-new-variant
```

### 4. Update Documentation

If your changes affect user-facing functionality:

- Update relevant package documentation in `docusaurus/docs/packages/`
- Update the getting started guide if needed
- Update the main README.md
- When adding a Slurm version, update the version lists in the README, the [Overview](./index.md) and the [Slurm package page](./packages/slurm.md)

### 5. Commit Changes

Commits follow [Conventional Commits](https://www.conventionalcommits.org/), and CI
checks every commit in a pull request against `.commitlintrc.yml`:

```bash
git add .
git commit -m "feat(slurm): add slurm 26.05.5

- Add the 26-05-5-1 version and its sha256
- Update the version lists in the docs
"
```

Commit message guidelines:

- Header: `<type>[(<scope>)]: <summary>`, where the type is one of `fix`, `feat`,
  `chore`, `security`, `ci`, `docs`, `test`, `refactor`, `perf`, `release` or
  `cherry-pick`
- Lowercase summary of at most 80 characters, with no trailing period
- Blank line, then detailed description if needed
- Signal a breaking change with a `BREAKING CHANGE:` footer, never `type!:`
- Reference issue numbers when applicable

Before pushing, run the same checks CI runs:

```bash
just check       # lint, typecheck and tests
just docs-build  # the docs site, including the generated package reference
```

### 6. Push and Create Pull Request

```bash
git push origin fix/slurm-s2n-rpath
```

Then create a pull request on GitHub with:

- Clear title describing the change
- Detailed description of what and why
- Any testing performed
- Related issue numbers (e.g., "Fixes #123")

## Package Development Guidelines

### Package Structure

Follow Spack conventions:

```python
class PackageName(AutotoolsPackage):
    """Brief description."""
    
    homepage = "https://..."
    url = "https://..."
    
    license("LICENSE-TYPE")
    
    version("X.Y.Z", sha256="...")
    
    variant("name", default=False, description="...")
    
    depends_on("dependency", type=("build", "link", "run"))
    
    def configure_args(self):
        args = []
        # Add configure arguments
        return args
```

### Coding Standards

- Code is formatted and linted with Ruff (`just fmt` applies it, `just lint` checks it), with a line length of 110
- Spelling is checked with codespell, and types with Pyright (`just typecheck`)
- Add comments for non-obvious logic
- Include docstrings for complex methods

### Testing

Before submitting:

```bash
# Audit the package and check it concretizes
spack audit packages slurm_factory.slurm
spack spec slurm_factory.slurm@version

# Test with multiple compilers (if applicable)
spack install slurm_factory.slurm@version %gcc@11
spack install slurm_factory.slurm@version %gcc@13

# Test variants
spack install slurm_factory.slurm@version +variant1
spack install slurm_factory.slurm@version ~variant1
```

### Documentation

- Update package documentation in `docusaurus/docs/packages/`
- Keep the class docstring in `package.py` current: the
  [Package Reference](./package-reference/index.md) is generated from it on every docs build
- Include examples of new variants
- Document any special configuration requirements
- Update version tables

## Code Review Process

1. Maintainers will review your pull request
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR
4. Your changes reach Slurm Factory once they are in a [release](./releasing.md): Slurm Factory pins this repository to a release tag (`SLURM_FACTORY_SPACK_REPO_TAG` in its `slurm_factory/constants.py`), so a merge to `main` alone does not change its builds

## Reporting Issues

When reporting bugs:

- Check existing issues first
- Include Spack version, OS, and error messages
- Provide steps to reproduce
- Include relevant logs

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0, the same license as the project.

## Code of Conduct

Be respectful and constructive in all interactions. We aim to maintain a welcoming community for all contributors.

## Questions?

If you have questions about contributing:

- Open a [GitHub Discussion](https://github.com/vantagecompute/slurm-factory-spack-repo/discussions)
- Check the [Contact page](./contact.md) for other ways to get in touch

## Thank You

Your contributions help make this project better for everyone. Thank you for taking the time to contribute!
