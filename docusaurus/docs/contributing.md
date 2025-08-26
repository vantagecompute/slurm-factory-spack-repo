# Contributing

Thank you for your interest in contributing to the Slurm Factory Spack Repository! This guide will help you get started.

## Ways to Contribute

There are many ways to contribute:

- 🐛 **Report bugs** - Help us identify and fix issues
- 💡 **Suggest features** - Propose new packages or variants
- 📝 **Improve documentation** - Fix typos, clarify instructions, add examples
- 🔧 **Submit patches** - Fix bugs or add features
- 🧪 **Test packages** - Verify builds on different platforms
- 📦 **Add packages** - Contribute new package definitions

## Getting Started

### Prerequisites

- Git and GitHub account
- Spack installed locally
- Familiarity with Spack package development
- Basic understanding of Python

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR-USERNAME/slurm-factory-spack-repo.git
cd slurm-factory-spack-repo
```

1. Add the upstream remote:

```bash
git remote add upstream https://github.com/vantagecompute/slurm-factory-spack-repo.git
```

## Development Workflow

### 1. Create a Branch

Create a descriptive branch for your changes:

```bash
git checkout -b fix/slurm-ipmi-variant
# or
git checkout -b feature/add-new-package
# or
git checkout -b docs/update-getting-started
```

### 2. Make Changes

Edit the package files in `spack_repo/slurm_factory/packages/`.

### 3. Test Your Changes

Add the repository and test your changes:

```bash
# Add your local repository
spack repo add $(pwd)/spack_repo/slurm_factory

# Test installation (dry run)
spack spec slurm@25-11-0-1 +your-new-variant

# Test actual build (if needed)
spack install --test=root slurm@25-11-0-1 +your-new-variant
```

### 4. Update Documentation

If your changes affect user-facing functionality:

- Update relevant package documentation in `docusaurus/docs/packages/`
- Update the getting started guide if needed
- Update the main README.md

### 5. Commit Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add IPMI variant to Slurm package

- Add +ipmi variant for FreeIPMI support
- Add freeipmi dependency
- Add --with-freeipmi configure argument
- Update package documentation
"
```

Commit message guidelines:

- Use present tense ("Add feature" not "Added feature")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed
- Reference issue numbers when applicable

### 6. Push and Create Pull Request

```bash
git push origin fix/slurm-ipmi-variant
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

- Follow PEP 8 Python style guidelines
- Use 4 spaces for indentation (no tabs)
- Keep lines under 100 characters when possible
- Add comments for non-obvious logic
- Include docstrings for complex methods

### Testing

Before submitting:

```bash
# Check package syntax
spack install --test=root --dry-run slurm@version

# Test with multiple compilers (if applicable)
spack install slurm@version %gcc@11
spack install slurm@version %gcc@13

# Test variants
spack install slurm@version +variant1
spack install slurm@version ~variant1
```

### Documentation

- Update package documentation in `docusaurus/docs/packages/`
- Include examples of new variants
- Document any special configuration requirements
- Update version tables

## Code Review Process

1. Maintainers will review your pull request
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR
4. Your changes will be included in the next release

## Reporting Issues

When reporting bugs:

- Check existing issues first
- Use the issue template
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
- Check the [Contact page](./contact) for other ways to get in touch

## Thank You

Your contributions help make this project better for everyone. Thank you for taking the time to contribute!
