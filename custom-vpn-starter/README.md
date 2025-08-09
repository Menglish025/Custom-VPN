
# Custom-VPN

A pragmatic, security-first VPN you can run today (WireGuard-based), with a clear path to **post-quantum/hybrid crypto** for the control plane.

This repo ships a minimal-but-solid baseline you can deploy in minutes, plus an R&D track for adding ML‑KEM (Kyber) / ML‑DSA (Dilithium)–based key management later.

---

## Why this design

- **Data plane now:** WireGuard (NoiseIK, X25519, ChaCha20‑Poly1305, BLAKE2s). It's small, fast, and audited.
- **Control plane future:** A separate “key‑broker” service that does authenticated key distribution and **rotates WireGuard keys** using a **TLS 1.3 PQ‑hybrid** channel (via OQS‑OpenSSL). Hybrid KEM: X25519 + ML‑KEM (Kyber). Signatures: Ed25519 + ML‑DSA.
- **Smart routing:** Optional client agent for split‑tunnel and domain/app rules.
- **Kill switch + DNS:** System firewall rules block leaks; DNS goes over the tunnel with ad/malware blocking.
- **Obfuscation:** Pluggable UDP disguises for hostile networks (e.g., UDP‑over‑QUIC wrapper or simple UDP2TCP).

> ⚠️ We **do not** invent cryptography. We compose audited primitives, and keep PQ experiments isolated until stable.

---

## Quick start (single server, one client)

### 0) Requirements
- Linux host with Docker & docker-compose (or Podman + compose). 
- A public IP or DNS name.
- UDP 51820 open on the server firewall.

### 1) Clone and configure
```bash
git clone <your-fork-url> Custom-VPN
cd Custom-VPN
python3 scripts/gen_wg_config.py     --server-endpoint vpn.example.com:51820     --client-name matt-pc     --server-ip 10.8.0.1/24     --client-ip 10.8.0.2/32
```

This writes a `server/wg0.conf` and a client file `clients/matt-pc.conf`.

### 2) Bring up the server
```bash
cd server
docker compose up -d
# or: docker-compose up -d
```

### 3) Install the client
- **Windows/macOS/Linux:** Install the official WireGuard app.
- Import `clients/matt-pc.conf` (QR or file). 
- Activate the tunnel.

### 4) Enforce kill‑switch + DNS (Windows example)
Open PowerShell as Administrator:
```powershell
# Blocks all non‑tunnel egress for the active interface named "WireGuard Tunnel"
.\client\windows\setup.ps1 -InterfaceName "WireGuard Tunnel" -Dns "10.8.0.1"
```
(Inspect the script before running. It uses native firewall/cmdlets; no downloads.)

---

## Repo map

```
server/                  # Dockerized WireGuard server + healthcheck
  docker-compose.yml
  wg0.conf               # generated; template lives in templates/
client/
  windows/setup.ps1      # kill switch & DNS pinning; split-tunnel rules (optional)
  routing-rules.json     # example domain/app routing config
clients/                 # generated client .conf files live here (gitignored)
pqc/
  README.md              # PQ hybrid plan + milestones
  keybroker/             # (future) Rust service skeleton for PQ TLS key rotation
scripts/
  gen_wg_config.py       # keypair + conf generator (server & clients)
templates/
  wg0.conf.j2
  wg-client.conf.j2
ROADMAP.md               # delivery plan
LICENSE
.gitignore
```

---

## Security posture (baseline)

- Small attack surface (WireGuard only; no SSH exposure required).
- Strict firewall: UDP 51820 only; default DROP.
- DNS forced through the tunnel; optional blocklists (AdGuard/Unbound upstreams).
- Automatic key/gen confs; no private keys in Git.
- Optional: multihop by peering two servers and routing subnets.

---

## Post‑quantum track (experimental)

The plan is to keep **WireGuard as the data plane** and build a **key‑broker** that:
1. Authenticates clients with classical+PQ signatures.
2. Establishes a **TLS 1.3 hybrid** channel (X25519+ML‑KEM) using OQS‑OpenSSL.
3. Issues short‑lived WireGuard static keys and rotates them on a schedule or on demand.
4. Publishes revocation and session metadata with minimal PII.
5. (Later) adds QUIC transport for NAT‑punchy control traffic.

Until hybrid TLS is production‑ready on your platform, run the classic baseline and track PQ progress in `pqc/`.

---

## Smart routing

Place your rules in `client/routing-rules.json` (domain, CIDR, or app path). The Windows script includes examples of per‑route additions via `New‑NetRoute` and `netsh interface portproxy` for special cases. A Rust/Go cross‑platform agent is a planned enhancement.

---

## License
MIT — see LICENSE.
