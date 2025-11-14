# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub repository automation scripts
  - Bootstrap script for initializing and pushing repository (`tools/bootstrap-repo.sh`, `tools/bootstrap-repo.ps1`)
  - Local development setup script (`tools/setup-local.sh`)
  - Environment validation script (`tools/check-env.sh`)
- GitHub Actions CI/CD workflows
  - CI/CD pipeline for testing, building, and publishing (`ci-cd.yml`)
  - Bare metal deployment workflow (`deploy-bare.yml`)
  - Duplicate file checker workflow (existing, maintained)
- GitHub issue templates
  - Bug report template
  - Feature request template
  - Documentation issue template
  - Issue config with helpful links
- Pull request template with comprehensive checklist
- CODEOWNERS file for automatic review assignments
- Dependabot configuration for dependency updates
- SECURITY.md with security policy and reporting guidelines
- Comprehensive README updates with bootstrap and setup instructions

### Changed
- Enhanced README.md with detailed GitHub setup instructions
- Updated documentation structure

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- Added security policy documentation
- Added environment validation checks

---

## [1.0.0] - YYYY-MM-DD (Template for future releases)

### Added
- Initial release of Neo Godmode Master Toolkit
- Baremetal, Pro, and Ultra kits
- Docker Compose configurations
- FastAPI Actions endpoints
- OpenAI API skeleton
- Orchestrator with council-of-experts pattern
- VS Code extension
- Installation scripts
- Documentation

---

## How to Update This Changelog

When making changes, update the [Unreleased] section with:

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

When releasing a new version:

1. Change [Unreleased] to the version number and date
2. Add a new [Unreleased] section at the top
3. Update the version links at the bottom

---

[Unreleased]: https://github.com/Kydras8/neo-godmode-master/compare/v1.0.0...HEAD
