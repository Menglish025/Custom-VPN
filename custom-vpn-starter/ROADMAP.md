
# Roadmap

## Phase 1 — Baseline VPN (this repo)
- [x] Dockerized WireGuard server
- [x] Config generator for server + clients
- [x] Kill switch + DNS pinning (Windows script)
- [ ] Optional ad/malware blocking via DoH upstreams
- [ ] Obfuscation plugin (UDP‑over‑QUIC wrapper as sidecar)

## Phase 2 — Smart Routing Agent
- [ ] Cross‑platform agent (Rust) to apply split‑tunnel by domain/app
- [ ] UI to toggle routes and measure latency/loss/throughput per route
- [ ] Auto‑failover between servers; health‑based selection

## Phase 3 — PQ‑Hybrid Control Plane
- [ ] Rust “keybroker” service with OQS‑OpenSSL TLS 1.3 hybrid (X25519+ML‑KEM)
- [ ] Client authentication: Ed25519 + ML‑DSA
- [ ] Short‑lived WG keys; rotation & revocation protocol
- [ ] Audit log with privacy filters
- [ ] Rollout plan and fallback to classical if PQ unavailable

## Phase 4 — Extras
- [ ] Multi‑hop / mesh (peer server chaining)
- [ ] Mobile apps with embedded rules
- [ ] Zero‑touch bootstrap using device‑bound codes
