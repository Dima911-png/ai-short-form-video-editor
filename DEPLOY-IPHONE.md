# Use AI Short-Form Video Editor from an iPhone

This repository includes a Dockerfile and Render Blueprint so the React app and FFmpeg backend can be deployed as one web service.

## What the app does

- Upload a short clip to a project.
- Transcribe speech and generate timed captions with Groq Whisper.
- Ask Gemini to plan punch-in zooms, caption emphasis, and relevant B-roll suggestions.
- Search and attach stock footage through Pexels.
- Render MP4 with FFmpeg.

This is an AI-assisted editor, not a guaranteed one-click professional edit: the current app has an interactive timeline and some B-roll steps still require review.

## Deploy from an iPhone

1. Open https://render.com/ and sign in.
2. Choose New +, then Blueprint, and connect this GitHub repository.
3. Review the service from render.yaml and create it.
4. In the Render service Environment settings, add API keys: GROQ_API_KEY from https://console.groq.com; GEMINI_API_KEY from https://aistudio.google.com/apikey; and optionally PEXELS_API_KEY from https://www.pexels.com/api/ for stock-media search.
5. Wait for the Docker build and deploy to finish. Open the service's onrender.com URL on your iPhone.

Never put API keys into source code, README files, or screenshots.

## Important free-tier limitations

- The Render free web service may sleep when idle and has limited compute and monthly hours.
- The Blueprint uses temporary storage under /tmp; projects, uploads, and renders can be lost when the service restarts or redeploys. Do not treat this as permanent storage.
- Groq, Gemini, and Pexels have their own quotas and terms. A free API key does not mean unlimited use.
- FFmpeg rendering is CPU- and memory-intensive; very large/high-resolution clips may fail on a free instance.
- The app currently has no user authentication. Do not upload private or sensitive footage to a publicly accessible deployment.

## Health check

After deployment, open /api/health on the service domain. A healthy service returns JSON with status: ok.

## Local development

See README.md for the full Python/Node setup. This deployment lets the UI and API run together without a local computer, but the hosting provider still supplies the compute.
