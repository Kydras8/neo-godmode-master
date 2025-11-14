# GitHub Automation Architecture

This document illustrates the automation architecture and workflows added to the Neo Godmode repository.

## Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      NEO GODMODE AUTOMATION                         │
└─────────────────────────────────────────────────────────────────────┘

   Developer          GitHub Actions           Production
      │                    │                        │
      ├─── Push Code ──────┤                        │
      │                    │                        │
      │              ┌─────▼─────┐                  │
      │              │  CI/CD    │                  │
      │              │ Pipeline  │                  │
      │              └─────┬─────┘                  │
      │                    │                        │
      │              ┌─────▼─────┐                  │
      │              │   Test    │                  │
      │              │   Lint    │                  │
      │              │   Build   │                  │
      │              └─────┬─────┘                  │
      │                    │                        │
      │              ┌─────▼─────┐                  │
      │              │  Publish  │                  │
      │              │   GHCR    │                  │
      │              └─────┬─────┘                  │
      │                    │                        │
      │              ┌─────▼─────┐                  │
      │              │ Security  │                  │
      │              │   Scan    │                  │
      │              └─────┬─────┘                  │
      │                    │                        │
      ├─ Manual Deploy ────┤                        │
      │                    │                        │
      │              ┌─────▼─────┐                  │
      │              │  Deploy   │                  │
      │              │ Workflow  │                  │
      │              └─────┬─────┘                  │
      │                    │                        │
      │                    ├─── SSH Deploy ─────────▼──
      │                    │
      │              ┌─────▼─────┐
      │              │Dependabot │
      │              │  Updates  │
      │              └───────────┘
```

## Repository Setup Flow

```
┌──────────────┐
│ Clone Repo   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ bootstrap-repo   │  ◄── Initialize git, add remote, push
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ setup-local      │  ◄── Install deps, create dirs, configure
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ check-env        │  ◄── Validate configuration
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Ready to develop │
└──────────────────┘
```

## CI/CD Pipeline Flow

```
Push to main/master or PR
         │
         ▼
┌─────────────────────┐
│   Checkout Code     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Install Deps      │
└─────────┬───────────┘
          │
          ├──────────────┐
          │              │
          ▼              ▼
┌──────────────┐  ┌──────────────┐
│   Lint       │  │  Run Tests   │
│  (flake8)    │  │  (pytest)    │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                │
                ▼
       ┌────────────────┐
       │ Duplicate Check│
       └────────┬───────┘
                │
                ▼
        [On main/master only]
                │
                ▼
       ┌────────────────┐
       │  Build Docker  │
       │     Image      │
       └────────┬───────┘
                │
                ▼
       ┌────────────────┐
       │   Push to      │
       │     GHCR       │
       └────────┬───────┘
                │
                ▼
       ┌────────────────┐
       │ Security Scan  │
       │    (Trivy)     │
       └────────┬───────┘
                │
                ▼
       ┌────────────────┐
       │Upload to Sec   │
       │    Dashboard   │
       └────────────────┘
```

## Deployment Flow

```
Manual Trigger or Push
         │
         ▼
┌─────────────────────┐
│  Create .env file   │
│  from secrets       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Setup SSH Key     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  rsync files to     │
│  remote server      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Copy .env to       │
│  server             │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  docker compose up  │
│  --build            │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Health Check       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Cleanup secrets    │
└─────────────────────┘
```

## Issue Management Flow

```
User creates issue
         │
         ▼
    ┌────────┐
    │Template│
    │ Select │
    └────┬───┘
         │
    ┌────┴────┬───────────┬──────────────┐
    │         │           │              │
    ▼         ▼           ▼              ▼
┌───────┐ ┌────────┐ ┌────────┐ ┌──────────────┐
│  Bug  │ │Feature │ │  Docs  │ │ Custom Issue │
└───┬───┘ └───┬────┘ └───┬────┘ └──────┬───────┘
    │         │           │             │
    └─────────┴───────────┴─────────────┘
                    │
                    ▼
           ┌────────────────┐
           │ Auto-labeled   │
           └────────┬───────┘
                    │
                    ▼
           ┌────────────────┐
           │CODEOWNERS       │
           │notified         │
           └────────────────┘
```

## Dependency Update Flow

```
Weekly Schedule (Monday)
         │
         ▼
┌─────────────────────┐
│   Dependabot        │
│   Scans Deps        │
└─────────┬───────────┘
          │
    ┌─────┴─────┬─────────────┬───────────┐
    │           │             │           │
    ▼           ▼             ▼           ▼
┌────────┐  ┌────────┐  ┌─────────┐  ┌────────┐
│ Python │  │ Docker │  │ GitHub  │  │  npm   │
│  Deps  │  │ Images │  │ Actions │  │ (vscode)
└───┬────┘  └───┬────┘  └────┬────┘  └───┬────┘
    │           │             │           │
    └───────────┴─────────────┴───────────┘
                    │
                    ▼
           ┌────────────────┐
           │  Create PR     │
           │  with updates  │
           └────────┬───────┘
                    │
                    ▼
           ┌────────────────┐
           │  CI runs on    │
           │  PR            │
           └────────┬───────┘
                    │
                    ▼
           ┌────────────────┐
           │  CODEOWNERS    │
           │  review        │
           └────────────────┘
```

## Security Flow

```
Code Change
     │
     ▼
┌──────────────┐
│  Push Code   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  CodeQL Scan │
└──────┬───────┘
       │
       ├────────────┐
       │            │
       ▼            ▼
┌───────────┐  ┌───────────┐
│  Trivy    │  │Dependabot │
│   Scan    │  │  Alerts   │
└─────┬─────┘  └─────┬─────┘
      │              │
      └──────┬───────┘
             │
             ▼
    ┌────────────────┐
    │ Security Tab   │
    │   Alerts       │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │ Manual Review  │
    └────────┬───────┘
             │
             ▼
    ┌────────────────┐
    │   Fix Issues   │
    └────────────────┘
```

## File Organization

```
neo-godmode-master/
├── .github/
│   ├── workflows/
│   │   ├── ci-cd.yml              ◄── CI/CD automation
│   │   ├── deploy-bare.yml        ◄── Deployment automation
│   │   └── duplicate-check.yml    ◄── Duplicate scanner
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md          ◄── Bug template
│   │   ├── feature_request.md     ◄── Feature template
│   │   ├── documentation.md       ◄── Docs template
│   │   └── config.yml             ◄── Template config
│   ├── PULL_REQUEST_TEMPLATE.md   ◄── PR template
│   ├── CODEOWNERS                 ◄── Review automation
│   └── dependabot.yml             ◄── Dependency automation
├── docs/
│   ├── github-automation.md       ◄── Complete guide
│   ├── QUICKSTART.md              ◄── Quick start
│   └── readme*.md                 ◄── Existing docs
├── tools/
│   ├── bootstrap-repo.sh          ◄── Init script (bash)
│   ├── bootstrap-repo.ps1         ◄── Init script (PS)
│   ├── setup-local.sh             ◄── Setup script
│   ├── check-env.sh               ◄── Validation script
│   └── [other tools]              ◄── Existing tools
├── .gitignore                     ◄── Ignore rules
├── SECURITY.md                    ◄── Security policy
├── CHANGELOG.md                   ◄── Change log
└── README.md                      ◄── Updated docs
```

## Workflow Triggers

| Workflow | Triggers | Runs On |
|----------|----------|---------|
| CI/CD Pipeline | Push to main/master, All PRs | ubuntu-latest |
| Deploy Bare | Manual (workflow_dispatch), Push to main (specific paths) | ubuntu-latest |
| Duplicate Check | Push to main/master, All PRs | ubuntu-latest |
| Dependabot | Weekly schedule (Monday) | GitHub infrastructure |

## Permissions Matrix

| Workflow | Permissions |
|----------|-------------|
| lint-and-test | contents: read |
| build-and-publish | contents: read, packages: write |
| security-scan | contents: read, security-events: write |
| deploy | contents: read |

## Integration Points

```
┌──────────────────────────────────────────────┐
│           External Services                  │
├──────────────────────────────────────────────┤
│  • GitHub Container Registry (GHCR)          │
│  • GitHub Security Dashboard                 │
│  • GitHub Discussions                        │
│  • Remote Servers (via SSH)                  │
│  • Docker Hub (base images)                  │
│  • PyPI (Python packages)                    │
└──────────────────────────────────────────────┘
```

## Security Boundaries

```
┌────────────────────────────────────┐
│      Public Repository             │
│  ┌──────────────────────────────┐  │
│  │     Protected Branches       │  │
│  │  ┌────────────────────────┐  │  │
│  │  │  Encrypted Secrets     │  │  │
│  │  │  • API Keys            │  │  │
│  │  │  • SSH Keys            │  │  │
│  │  │  • Passwords           │  │  │
│  │  └────────────────────────┘  │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

## Summary

The automation architecture provides:

1. **Continuous Integration**: Automated testing and validation
2. **Continuous Deployment**: One-click deployment to production
3. **Security**: Automated vulnerability scanning and updates
4. **Quality**: Code review automation and templates
5. **Documentation**: Comprehensive guides and quick starts
6. **Maintenance**: Automated dependency updates

All workflows follow security best practices with minimal permissions and encrypted secrets handling.
