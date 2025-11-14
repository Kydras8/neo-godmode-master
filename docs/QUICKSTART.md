# GitHub Automation Setup - Quick Start

This document provides a quick start guide for the new GitHub automation features added to the Neo Godmode repository.

## What's New

This PR adds comprehensive automation to streamline repository management, development, and deployment workflows.

## Quick Start

### 1. Bootstrap Your Repository (First Time Setup)

If you're setting up a new Neo Godmode repository:

```bash
# Linux/macOS
cd tools
./bootstrap-repo.sh

# Windows
cd tools
.\bootstrap-repo.ps1
```

This will:
- Initialize git (if needed)
- Configure remote origin
- Create initial commit
- Push to GitHub

### 2. Set Up Local Development

```bash
cd tools
./setup-local.sh
```

This will:
- Check prerequisites (Python, Docker, Git)
- Create `.env` file from template
- Install Python dependencies
- Create necessary directories
- Validate configuration

### 3. Configure Environment

Edit your `.env` file with actual API keys:

```bash
# Location: kits/neo-godmode-baremetal-kit/neo-godmode/.env
OPENAI_API_KEY=your-actual-key
SERPAPI_API_KEY=your-actual-key
ACTIONS_API_KEY=generate-strong-password
JWT_SECRET=generate-random-secret
```

### 4. Validate Configuration

```bash
cd tools
./check-env.sh
```

This checks for:
- Required API keys
- Security settings
- Database configuration
- Production settings

## GitHub Actions Workflows

### Automatic CI/CD

Runs automatically on push to main/master and on all pull requests:

1. **Linting & Testing**
   - Python code linting with flake8
   - Duplicate file checking
   - Unit tests (if available)

2. **Building & Publishing** (main/master only)
   - Docker image build
   - Multi-platform support (amd64, arm64)
   - Publish to GitHub Container Registry

3. **Security Scanning** (main/master only)
   - Trivy vulnerability scanning
   - Results uploaded to Security tab

### Manual Deployment

Deploy to bare metal server:

1. Go to Actions tab
2. Select "Deploy to Bare Metal"
3. Click "Run workflow"
4. Choose environment (staging/production)

**Prerequisites:**
- Configure GitHub secrets (see below)
- Ensure server is accessible via SSH

## Required GitHub Secrets

### For CI/CD (Building & Publishing)
- `GITHUB_TOKEN` - Automatically provided

### For Deployment
Set these in: Settings → Secrets and variables → Actions

#### Required:
- `DEPLOY_SSH_KEY` - SSH private key for deployment
- `SSH_HOST` - Server hostname/IP
- `SSH_USER` - SSH username  
- `SSH_PATH` - Deployment path (e.g., `/opt/neo-godmode`)
- `OPENAI_API_KEY` - OpenAI API key
- `SERPAPI_API_KEY` - SerpAPI key
- `ACTIONS_API_KEY` - API key for actions endpoint
- `JWT_SECRET` - JWT signing secret
- `POSTGRES_PASSWORD` - Database password
- `DOMAIN` - Production domain
- `TRAEFIK_EMAIL` - Email for Let's Encrypt

#### Optional:
- `OPENAI_MODEL` - Default: `gpt-4o`
- `POSTGRES_USER` - Default: `neo`
- `POSTGRES_DB` - Default: `neo`

## Issue Templates

When creating issues, use the provided templates:

- **Bug Report**: Report bugs with environment details
- **Feature Request**: Suggest new features
- **Documentation**: Report documentation issues

## Pull Request Template

All PRs use a comprehensive template covering:
- Type of change
- Testing performed
- Security considerations
- Breaking changes
- Documentation updates

## Code Ownership

CODEOWNERS file ensures:
- @Kydras8 reviews all changes
- Automatic review requests
- Extra scrutiny on sensitive files

## Dependency Updates

Dependabot automatically:
- Updates Python dependencies weekly
- Updates Docker images weekly
- Updates GitHub Actions weekly
- Creates PRs with updates
- Labels PRs appropriately

## Security

### Reporting Vulnerabilities

Use GitHub Security Advisories:
https://github.com/Kydras8/neo-godmode-master/security/advisories/new

### Best Practices

1. Never commit secrets to git
2. Use strong passwords and secrets
3. Enable 2FA on GitHub
4. Review Dependabot PRs promptly
5. Monitor security alerts
6. Keep dependencies updated

## Files Added

### Scripts
- `tools/bootstrap-repo.sh` - Bash bootstrap script
- `tools/bootstrap-repo.ps1` - PowerShell bootstrap script
- `tools/setup-local.sh` - Local development setup
- `tools/check-env.sh` - Environment validation

### GitHub Configuration
- `.github/workflows/ci-cd.yml` - CI/CD pipeline
- `.github/workflows/deploy-bare.yml` - Deployment workflow
- `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report template
- `.github/ISSUE_TEMPLATE/feature_request.md` - Feature template
- `.github/ISSUE_TEMPLATE/documentation.md` - Documentation template
- `.github/ISSUE_TEMPLATE/config.yml` - Issue config
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template
- `.github/CODEOWNERS` - Code ownership rules
- `.github/dependabot.yml` - Dependency automation

### Documentation
- `SECURITY.md` - Security policy
- `CHANGELOG.md` - Change tracking
- `docs/github-automation.md` - Complete automation guide
- `.gitignore` - Git ignore rules
- Updated `README.md` - Bootstrap instructions

## Troubleshooting

### Bootstrap script fails
- Check git is installed: `git --version`
- Verify GitHub credentials are configured
- Ensure repository exists on GitHub

### Setup script fails
- Check Python is installed: `python3 --version`
- Verify network access for pip
- Check directory permissions

### Workflow fails
- Check GitHub Actions tab for logs
- Verify secrets are configured
- Check workflow syntax with YAML validator

### Deployment fails
- Verify SSH key has no passphrase
- Check server is accessible: `ssh user@host`
- Verify docker-compose.yml exists on server
- Review deployment logs

## Getting Help

- Check [docs/github-automation.md](docs/github-automation.md) for detailed guide
- Review workflow logs in Actions tab
- Create issue using templates
- Contact maintainers via discussions

## Next Steps

1. Run bootstrap script to initialize repository
2. Set up local development environment
3. Configure environment variables
4. Add GitHub secrets for deployment
5. Test workflows by creating a PR
6. Review security policy
7. Enable Dependabot alerts

---

For more information, see:
- [Complete Automation Guide](docs/github-automation.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
