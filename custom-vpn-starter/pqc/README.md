
# PQ‑Hybrid Control Plane (R&D)

**Objective:** keep WireGuard for data, add a separate authenticated channel for key rotation that uses **TLS 1.3 hybrid** (classical + post‑quantum).

## Components
- **keybroker (Rust):** gRPC/JSON API over TLS 1.3 (OQS‑OpenSSL).
- **client‑agent (Rust):** Talks to keybroker, installs fresh WG keys, triggers rotation.
- **CA & identities:** Ed25519 + ML‑DSA (Dilithium) for offline issuance.

## Milestones
1. Build OQS‑OpenSSL and produce a minimal TLS client/server demo.
2. Define a key issuance schema: device ID, peer pubkey, expiry, revocation.
3. Implement rotation policy (time/volume-based).
4. Integrate with WireGuard via `wg set` / UAPI for live reload.
5. Hardening, logging, and audits.

> Keep this branch **isolated** from production until libraries are stable on your OS targets.
