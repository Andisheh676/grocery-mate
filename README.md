# grocery-mate

## Security

This repository implements security best practices to prevent accidental exposure of sensitive information:

### Protected File Types
The following types of files are automatically excluded from commits via `.gitignore`:
- SSH keys (*.pem, *.key, id_rsa*, etc.)
- Environment files (.env, .env.local, etc.)
- API credentials and tokens
- Service account files

### Secret Scanning
This repository uses Gitleaks configuration (`.gitleaks.toml`) to detect:
- OpenSSH private keys
- RSA/EC private keys
- API keys
- AWS credentials
- Other common secrets

### Best Practices
1. **Never commit credentials** - Use environment variables or secure vaults
2. **Use .env files** for local development (these are gitignored)
3. **Rotate any exposed credentials immediately**
4. **Use secret scanning tools** before pushing code

### If You Accidentally Commit a Secret
1. **Immediately rotate/revoke the credential**
2. **Remove it from git history** using tools like BFG Repo-Cleaner or git-filter-repo
3. **Force push the cleaned history** (coordinate with team)
4. **Scan for any unauthorized access** using the exposed credential