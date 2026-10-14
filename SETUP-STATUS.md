## Current setup status

The repository contains the original AI Short-Form Video Editor plus Docker and Render deployment files. GitHub Actions is configured to build the frontend and Docker image on pushes. A successful deployment has not yet been confirmed.

### Security before public use

The upstream app has no user authentication. Do not expose it publicly with personal API keys until access control is added. Otherwise, anyone who discovers the service URL may be able to use its editing endpoints and consume the configured API quotas.

### Free hosting caveats

Render free instances sleep after inactivity and have an ephemeral filesystem. Uploaded videos, projects, and renders can disappear after a restart, sleep, or redeploy. API provider quotas also apply, and free compute is not unlimited.
