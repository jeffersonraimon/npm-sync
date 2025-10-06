# npm-sync

`npm-sync` synchronizes **Proxy Hosts** from a source Nginx Proxy Manager (NPM) to one or more destination instances in **mirror mode**. It runs inside a Docker container and can be scheduled to run periodically (default: every 12 hours).

Features
- Unidirectional mirror from source → destination(s) for **Proxy Hosts**.
- Create, update and delete entries on destination so it matches the source (mirror mode).
- Multi-target support (one or more destinations).
- Runs periodically (configurable interval).
- Colored logs (added / updated / deleted).
- Simple configuration via `config.yml`.

## Quick start

1. Copy `config.example.yml` to `config.yml` and edit the host and credentials.
2. Build the image:
```bash
docker build -t ghcr.io/jeffersonraimon/npm-sync:latest .
```
3. Run (bind your config):
```bash
docker run -d -v $(pwd)/config.yml:/app/config.yml --name npm-sync ghcr.io/jeffersonraimon/npm-sync:latest
```

Or use the provided image name in GHCR once published: `ghcr.io/jeffersonraimon/npm-sync`.

## Files
- `main.py` — entrypoint and loop
- `api.py` — small NPM API client
- `sync.py` — synchronization logic
- `utils.py` — helpers and colored logging
- `config.example.yml` — example configuration
- `docker-compose.example.yml` — docker compose example configuration
- `Dockerfile`, `requirements.txt`, `LICENSE`

