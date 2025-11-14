# GitHub Automation Guide

This document describes all the GitHub automation features available in the Neo Godmode repository.

## Table of Contents

- [Repository Setup](#repository-setup)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Issue Management](#issue-management)
- [Dependency Management](#dependency-management)
- [Security](#security)

## Repository Setup

### Bootstrap Scripts

Bootstrap scripts help you initialize and push the repository to GitHub.

#### Usage

**Linux/macOS:**
```bash
cd tools
./bootstrap-repo.sh
```

**Windows:**
```powershell
cd tools
.\bootstrap-repo.ps1
```

#### What it does:
1. Initializes git repository (if needed)
2. Prompts for GitHub repository URL
3. Adds remote origin
4. Creates initial commit
5. Pushes to GitHub

### Local Development Setup

Set up your local development environment with all dependencies.

#### Usage

```bash
cd tools
./setup-local.sh
```

#### What it does:
1. Checks for required tools (Python, Docker, Git)
2. Creates `.env` file from template
3. Installs Python dependencies for all components
4. Creates necessary directories (data, logs, deliverables)
5. Validates basic configuration

### Environment Validation

Validate your `.env` configuration before running services.

#### Usage

```bash
cd tools
./check-env.sh
```

#### What it checks:
- Required API keys (OpenAI, SerpAPI)
- Security settings (JWT secrets, API keys)
- Database configuration
- Production settings (domain, email)

## GitHub Actions Workflows

### CI/CD Pipeline (`ci-cd.yml`)

Runs on every push to main/master branches and on all pull requests.

#### Jobs:

1. **lint-and-test**
   - Runs Python linting with flake8
   - Executes duplicate file checker
   - Runs tests (if they exist)
   - Uploads duplicate report as artifact

2. **build-and-publish** (only on main/master push)
   - Builds Docker images for Actions service
   - Publishes to GitHub Container Registry (GHCR)
   - Supports multi-platform builds (amd64, arm64)
   - Uses build caching for faster builds

3. **security-scan** (only on main/master push)
   - Runs Trivy vulnerability scanner
   - Uploads results to GitHub Security tab
   - Scans filesystem for vulnerabilities

#### Required Secrets:
- `GITHUB_TOKEN` (automatically provided)

#### Optional Secrets (for publishing):
- `GHCR_USER` - GitHub username
- `GHCR_TOKEN` - Personal access token with packages:write

### Bare Metal Deployment (`deploy-bare.yml`)

Deploys the application to a remote server via SSH.

#### Trigger:
- Manual via workflow_dispatch
- Automatic on push to main (for specific paths)

#### Required Secrets:
- `DEPLOY_SSH_KEY` - SSH private key
- `SSH_HOST` - Server hostname or IP
- `SSH_USER` - SSH username
- `SSH_PATH` - Deployment path on server
- `OPENAI_API_KEY`
- `SERPAPI_API_KEY`
- `ACTIONS_API_KEY`
- `JWT_SECRET`
- `DOMAIN`
- `TRAEFIK_EMAIL`
- `POSTGRES_PASSWORD`

#### What it does:
1. Creates `.env` file with secrets
2. Syncs repository files to server via rsync
3. Deploys using docker-compose.bare.yml
4. Performs health checks
5. Cleans up sensitive files

### Duplicate File Checker (`duplicate-check.yml`)

Scans for duplicate files across the repository.

#### Trigger:
- Push to main/master
- All pull requests

#### Output:
- Uploads duplicate report as artifact
- Report available for 30 days

## Issue Management

### Issue Templates

We provide three issue templates to help structure bug reports, feature requests, and documentation issues.

#### Bug Report Template
Use this for reporting bugs or issues.

**Includes:**
- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Logs and error messages
- Screenshots

#### Feature Request Template
Use this for suggesting new features.

**Includes:**
- Feature description
- Problem statement
- Proposed solution
- Use cases
- Implementation considerations
- Priority level

#### Documentation Issue Template
Use this for documentation improvements.

**Includes:**
- Location of issue
- Description of problem
- Suggested improvements

### Issue Configuration

The repository includes helpful links:
- 📚 Documentation
- 💬 Discussions
- 🔒 Security Issues

### Pull Request Template

Comprehensive PR template ensures quality contributions.

**Sections:**
- Type of change
- Related issues
- Changes made
- Testing performed
- Kit impact analysis
- Security considerations
- Breaking changes
- Documentation updates
- Deployment notes

## Dependency Management

### Dependabot Configuration

Automatic dependency updates are configured for:

1. **Python Dependencies** (pip)
   - Actions service
   - API service
   - Orchestrator service
   - Weekly updates on Monday

2. **Docker Images**
   - Base images in Dockerfiles
   - Weekly updates on Monday

3. **GitHub Actions**
   - Action versions in workflows
   - Weekly updates on Monday

### Configuration:
- Max 5 open PRs for Python dependencies
- Max 3 open PRs for Docker and Actions
- All PRs reviewed by @Kydras8
- Auto-labeled with dependency type
- Conventional commit format with [deps] prefix

## Security

### CODEOWNERS

Automatic review requests for sensitive files:
- All files default to @Kydras8
- Canonical kit files
- GitHub Actions workflows
- Documentation
- Environment examples
- Docker compose files
- Deployment scripts

### Security Policy (SECURITY.md)

Comprehensive security guidelines:
- Vulnerability reporting process
- Response timeline
- Security best practices
- Known security considerations
- Disclosure policy

### Security Best Practices

1. **API Keys**: Never commit secrets, use `.env` files
2. **Strong Secrets**: Change all defaults in production
3. **HTTPS**: Always use TLS in production
4. **Authentication**: Use JWT with proper scopes
5. **Monitoring**: Set up logging and alerts
6. **Updates**: Keep dependencies current
7. **Backups**: Regular data backups
8. **Network**: Use firewalls and restrict ports
9. **Permissions**: Principle of least privilege
10. **Reviews**: Regular security audits

## Tips and Tricks

### Running Workflows Locally

Test GitHub Actions workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run CI workflow
act -j lint-and-test

# Run with secrets
act -j lint-and-test --secret-file .secrets
```

### Monitoring Workflow Runs

View workflow runs:
- Go to Actions tab in GitHub
- Click on specific workflow
- Review logs and artifacts

### Managing Secrets

Add secrets via GitHub UI:
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value
4. Save

### Customizing Workflows

Edit workflow files in `.github/workflows/` to customize:
- Trigger conditions
- Job steps
- Environment variables
- Timeout values
- Permissions

### Skipping CI

Skip CI runs by including in commit message:
```
[skip ci]
or
[ci skip]
```

## Troubleshooting

### Common Issues

**Workflow fails on permissions:**
- Check repository settings → Actions → Permissions
- Ensure "Read and write permissions" is enabled

**Docker build fails:**
- Check Dockerfile paths in workflow
- Verify build context is correct
- Review Docker build logs

**Deployment fails:**
- Verify SSH key is correct (no passphrase)
- Check server is accessible from GitHub
- Verify docker-compose.yml path on server
- Review deployment logs

**Secrets not available:**
- Verify secrets are set in repository settings
- Check secret names match workflow references
- Ensure you're on the correct repository

### Getting Help

- Check workflow logs in Actions tab
- Review documentation in `/docs`
- Open an issue using provided templates
- Contact maintainers via discussions

## Contributing

When contributing automation improvements:

1. Test locally when possible
2. Document changes in this file
3. Update CHANGELOG.md
4. Follow PR template
5. Request review from CODEOWNERS

---

For more information, see:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [CODEOWNERS Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
