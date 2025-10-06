from typing import List, Dict, Any
from utils import info, action_added, action_updated, action_deleted, warn
import copy
# Helper to produce a minimal payload accepted by NPM for proxy-host create/update.
def minimal_host_payload(host: Dict[str, Any]) -> Dict[str, Any]:
    # Keep only fields that the API expects for proxy-hosts.
    payload = {}
    payload['domain_names'] = host.get('domain_names') or host.get('domains') or []
    payload['forward_scheme'] = host.get('forward_scheme', host.get('scheme','http'))
    payload['forward_host'] = host.get('forward_host') or host.get('forwarding_host') or host.get('forwardTo') or ''
    payload['forward_port'] = host.get('forward_port') or host.get('forwarding_port') or host.get('forwardToPort') or 80
    payload['access_list_id'] = int(host.get('access_list_id') or 0)
    payload['certificate_id'] = int(host.get('certificate_id') or 0)
    payload['ssl_forced'] = bool(host.get('ssl_forced', False))
    payload['caching_enabled'] = bool(host.get('caching_enabled', False))
    payload['block_exploits'] = bool(host.get('block_exploits', False))
    payload['advanced_config'] = host.get('advanced_config') or ''
    payload['meta'] = host.get('meta', { 'letsencrypt_agree': False })
    payload['allow_websocket_upgrade'] = bool(host.get('allow_websocket_upgrade', True))
    payload['http2_support'] = bool(host.get('http2_support', True))
    payload['enabled'] = bool(host.get('enabled', True))
    payload['locations'] = host.get('locations', [])
    payload['hsts_enabled'] = bool(host.get('hsts_enabled', False))
    payload['hsts_subdomains'] = bool(host.get('hsts_subdomains', False))
    return payload

def sync_proxy_hosts(src_client, dst_client, mirror: bool = True, dry_run: bool = False):
    info('Fetching source proxy hosts...')
    src_hosts = src_client.get_proxy_hosts()
    info(f'Found {len(src_hosts)} hosts in source')

    info('Fetching destination proxy hosts...')
    dst_hosts = dst_client.get_proxy_hosts()
    info(f'Found {len(dst_hosts)} hosts in destination')

    # Map destinations by canonical domain (first domain name)
    dst_map = {}
    for h in dst_hosts:
        names = h.get('domain_names') or []
        key = tuple(sorted(names))
        dst_map[key] = h

    src_keys = set()
    # Create or update
    for host in src_hosts:
        names = host.get('domain_names') or []
        key = tuple(sorted(names))
        src_keys.add(key)
        dst_existing = dst_map.get(key)
        payload = minimal_host_payload(host)

        if dst_existing is None:
            action_added(' '.join(names))
            if not dry_run:
                r = dst_client.create_proxy_host(payload)
                # optionally inspect r for errors
        else:
            # Compare relevant fields; if different, update
            # Use minimal payload for comparison
            dst_min = minimal_host_payload(dst_existing)
            if dst_min != payload:
                action_updated(' '.join(names))
                if not dry_run:
                    r = dst_client.update_proxy_host(dst_existing.get('id'), payload)
            else:
                info('Unchanged: ' + ','.join(names))

    # Mirror: delete hosts in dst that are not in src
    if mirror:
        for key, h in dst_map.items():
            if key not in src_keys:
                action_deleted(','.join(h.get('domain_names') or []))
                if not dry_run:
                    try:
                        dst_client.delete_proxy_host(h.get('id'))
                    except Exception as e:
                        warn(f'Failed to delete {h.get("id")}: {e}')
