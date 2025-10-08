# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please report it by:

1. **DO NOT** open a public issue
2. Email the maintainers directly (or use GitHub Security Advisories)
3. Provide detailed information about the vulnerability

## Credential Exposure Response

If you accidentally commit credentials:

### Immediate Actions
1. **Revoke/rotate the exposed credential immediately**
2. **DO NOT** just delete the file - the secret is in git history
3. **Check for unauthorized access** using the exposed credential
4. **Notify the team** if working in a shared repository

### Cleaning Git History
Remove secrets from git history using one of these tools:

#### Option 1: BFG Repo-Cleaner (Recommended)
```bash
# Download BFG
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

# Remove secrets (replace with your pattern)
java -jar bfg-1.14.0.jar --replace-text passwords.txt
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

#### Option 2: git-filter-repo
```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove file from history
git filter-repo --invert-paths --path path/to/secret/file

# Force push
git push --force
```

## Prevention Measures

This repository includes several security measures:

1. **`.gitignore`** - Excludes common sensitive file types
2. **`.gitleaks.toml`** - Configuration for secret scanning
3. **`.githooks/pre-commit`** - Pre-commit hook to detect secrets
4. **`SECURITY.md`** - This security policy

### Setting Up Pre-commit Hook

To enable the pre-commit hook:

```bash
git config core.hooksPath .githooks
```

Or copy it to your `.git/hooks/` directory:

```bash
cp .githooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

### Installing Gitleaks (Recommended)

For better secret detection, install Gitleaks:

```bash
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/
```

## Common Secrets to Avoid

- SSH private keys (`id_rsa`, `*.pem`, `*.key`)
- API keys and tokens
- Database credentials
- Cloud provider credentials (AWS, Azure, GCP)
- Password files
- Environment files with secrets (`.env`)
- Service account JSON files

## Best Practices

1. Use environment variables for secrets
2. Use secret management tools (HashiCorp Vault, AWS Secrets Manager, etc.)
3. Never hardcode credentials in source code
4. Regularly scan for secrets using automated tools
5. Review code before committing
6. Use `.env.example` files to show required environment variables (without values)
