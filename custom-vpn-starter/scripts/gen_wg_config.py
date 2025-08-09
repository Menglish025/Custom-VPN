#!/usr/bin/env python3
import argparse, os, base64, subprocess
from pathlib import Path

def b64(n=32):
    import os, base64
    return base64.b64encode(os.urandom(n)).decode().strip()

def derive_pub(priv_b64):
    # Prefer external `wg pubkey` for correctness, else require manual replacement.
    try:
        p = subprocess.run(["wg", "pubkey"], input=(priv_b64+"\n").encode(), capture_output=True, check=True)
        return p.stdout.decode().strip()
    except Exception:
        return "REPLACE_WITH_WG_PUBKEY"

def render(template, mapping):
    out = template
    for k,v in mapping.items():
        out = out.replace("{{ "+k+" }}", str(v))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--server-endpoint", required=True, help="host:port clients connect to")
    ap.add_argument("--server-ip", default="10.8.0.1/24")
    ap.add_argument("--client-name", required=True)
    ap.add_argument("--client-ip", default="10.8.0.2/32")
    ap.add_argument("--egress-iface", default="eth0")
    ap.add_argument("--dns-ip", default="10.8.0.1")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]
    tmpl_dir = repo / "templates"
    server_tpl = (tmpl_dir/"wg0.conf.j2").read_text()
    client_tpl = (tmpl_dir/"wg-client.conf.j2").read_text()

    server_priv = b64(32)
    server_pub = derive_pub(server_priv)

    client_priv = b64(32)
    client_pub = derive_pub(client_priv)
    psk = b64(32)

    server_cfg = render(server_tpl, {
        "server_ip": args.server_ip,
        "server_private_key": server_priv,
        "egress_iface": args.egress_iface
    })
    server_cfg += f\"\n[Peer]\n# {args.client_name}\nPublicKey = {client_pub}\nPresharedKey = {psk}\nAllowedIPs = {args.client_ip}\nPersistentKeepalive = 25\n\"

    (repo/'server').mkdir(exist_ok=True, parents=True)
    (repo/'server'/'wg0.conf').write_text(server_cfg)

    client_cfg = render(client_tpl, {
        "client_private_key": client_priv,
        "client_ip": args.client_ip,
        "dns_ip": args.dns_ip,
        "server_public_key": server_pub,
        "psk": psk,
        "endpoint": args.server_endpoint
    })
    (repo/'clients').mkdir(exist_ok=True, parents=True)
    (repo/'clients'/f\"{args.client_name}.conf\").write_text(client_cfg)

    print(\"Wrote server config -> server/wg0.conf\")
    print(f\"Wrote client config -> clients/{args.client_name}.conf\")

if __name__ == '__main__':
    main()
