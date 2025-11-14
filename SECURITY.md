# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via:

1. **GitHub Security Advisories** (preferred):
   - Go to https://github.com/Kydras8/neo-godmode-master/security/advisories/new
   - Provide detailed information about the vulnerability

2. **Private Email**:
   - Contact the maintainers directly
   - Include "SECURITY" in the subject line
   - Provide detailed steps to reproduce the issue

## What to Include

When reporting a security issue, please include:

- Type of issue (e.g., SQL injection, XSS, authentication bypass)
- Full paths of source file(s) related to the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies based on severity and complexity

## Security Best Practices

When using Neo Godmode:

1. **Never commit secrets**: Use `.env` files and keep them in `.gitignore`
2. **Use strong API keys**: Change all default passwords and secrets
3. **Keep dependencies updated**: Enable Dependabot and apply security patches
4. **Use HTTPS in production**: Always use TLS/SSL for production deployments
5. **Restrict API access**: Use JWT authentication and scope-based authorization
6. **Monitor logs**: Set up logging and monitoring for suspicious activity
7. **Regular backups**: Back up your data and configurations regularly
8. **Network security**: Use firewalls and restrict access to necessary ports only
9. **Update regularly**: Keep Docker images and system packages up to date
10. **Review permissions**: Follow principle of least privilege

## Known Security Considerations

### API Keys and Secrets
- The `.env.example` file contains placeholder values
- Never commit actual API keys to the repository
- Rotate secrets regularly, especially in production

### Docker Deployment
- Images are built from public base images
- Review Dockerfile security before production use
- Consider using private registries for production images

### JWT Authentication
- Default JWT secrets in `.env.example` are insecure
- Generate strong, random secrets for production
- Configure appropriate token expiration times

### Database Security
- Default database passwords must be changed
- Use strong passwords for PostgreSQL and other databases
- Restrict database network access

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find similar problems
3. Prepare fixes for all supported versions
4. Release patches as soon as possible

We ask that you:

- Give us reasonable time to fix the issue before public disclosure
- Make a good faith effort to avoid privacy violations, data destruction, and service interruption
- Do not exploit the vulnerability beyond what is necessary to demonstrate it

## Security Updates

Security updates will be released as:

- Patch releases for critical vulnerabilities
- Documentation updates for configuration issues
- Security advisories via GitHub Security Advisories

Stay informed:

- Watch this repository for security advisories
- Check the [GitHub Security tab](https://github.com/Kydras8/neo-godmode-master/security)
- Review release notes for security-related changes

## Credits

We appreciate security researchers who responsibly disclose vulnerabilities. If you report a valid security issue, we'll:

- Credit you in the security advisory (if desired)
- Keep you informed throughout the fix process
- Thank you publicly in release notes (with your permission)

---

Thank you for helping keep Neo Godmode and its users safe!
