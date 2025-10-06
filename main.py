import time, os, sys, signal
import yaml
from api import NPMClient
from sync import sync_proxy_hosts
from utils import info, warn, error

shutdown = False
def handle_sig(signum, frame):
    global shutdown
    info('Shutdown signal received, exiting...')
    shutdown = True

signal.signal(signal.SIGINT, handle_sig)
signal.signal(signal.SIGTERM, handle_sig)

def load_config(path='config.yml'):
    cfg_path = os.environ.get('NPM_SYNC_CONFIG', path)
    if not os.path.exists(cfg_path):
        print('Config file not found at %s' % cfg_path)
        sys.exit(1)
    with open(cfg_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    cfg = load_config()
    interval_hours = cfg.get('interval_hours', cfg.get('interval', 12))
    interval = int(interval_hours) * 3600
    mirror = cfg.get('mirror', True)
    dry_run = cfg.get('dry_run', False)

    source = cfg.get('source') or cfg.get('src') or cfg.get('origin')
    destinations = cfg.get('destinations') or cfg.get('targets') or cfg.get('destination') or []
    if not source or not destinations:
        print('Source and at least one destination must be defined in config.yml')
        sys.exit(1)

    # Support list of destinations
    if isinstance(destinations, dict):
        destinations = [destinations]

    info('Starting npm-sync (mirror=%s, interval_hours=%s, dry_run=%s)' % (mirror, interval_hours, dry_run))

    while not shutdown:
        try:
            src_client = NPMClient(source['host'], source['username'], source['password'])
        except Exception as e:
            error('Failed to login to source: %s' % e)
            if shutdown: break
            time.sleep(60); continue

        # iterate destinations and sync each
        for dst in destinations:
            try:
                dst_client = NPMClient(dst['host'], dst['username'], dst['password'])
            except Exception as e:
                warn('Failed to login to destination %s: %s' % (dst.get('host'), e))
                continue

            try:
                sync_proxy_hosts(src_client, dst_client, mirror=mirror, dry_run=dry_run)
            except Exception as e:
                warn('Sync error for %s: %s' % (dst.get('host'), e))

        # Sleep until next run OR break if shutdown requested
        for _ in range(int(interval/5)):
            if shutdown:
                break
            time.sleep(5)

    info('npm-sync exiting.')
if __name__ == '__main__':
    main()
