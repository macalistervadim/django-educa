# System Security

## Overview
Django Educa employs a multi-layered approach to security:
- Secret management via HashiCorp Vault
- Authentication through OAuth2 (Google, GitHub)
- HTTPS for data protection in transit
- Containerization for component isolation

## Secret Management

### HashiCorp Vault
- **Endpoint**: `http://localhost:8200`
- **UI Access**: Enabled
- **Storage**: File-based with auditing
- **Policies**: Restricted access per service

### Application Secrets
Vault stores sensitive data for:
- Django (SECRET_KEY, credentials)
- PostgreSQL
- Redis
- OAuth2 providers
- AWS/MinIO

## Authentication

### OAuth2 Providers
- Google OAuth2
- GitHub OAuth2
- Standard Django authentication

### Sessions and Tokens
- Session storage in Redis
- Secure and HttpOnly cookies

## Permissions and Access

### Django Permissions
- Model-level
- Object-level
- Custom permissions for courses

### API Security
- Throttling for API endpoints
- CORS settings
- CSRF protection

## Data Protection

### Storage
- Encryption of secrets in Vault
- Secure password storage (PBKDF2)
- S3-compatible storage (MinIO)

### Data Transmission
- HTTPS for external connections
- Internal Docker network for services
- TLS for Redis and PostgreSQL

## Security Monitoring

### Auditing
- Action logging in Vault
- Django security logs
- Nginx security logs

### Alerts
- Email notifications

## Recommendations

### Deployment
- Regular dependency updates
- Container vulnerability scanning
- Security configuration checks

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 
