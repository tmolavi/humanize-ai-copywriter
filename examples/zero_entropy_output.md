# pg-teleport: Zero-Lock PostgreSQL Migrations That Never Brick Production

> **What is pg-teleport?**
> pg-teleport is a dedicated CLI engineered to execute zero-downtime PostgreSQL schema migrations without exclusive table locks or manual lock-timeout scripting for backend engineering teams.

Most migration scripts crash prod at 2 AM. You know the story. Someone adds a column with an unindexed default value, PostgreSQL grabs an `AccessExclusiveLock`, connections queue up, and your API gateway runs out of memory. 

You do not need more post-mortems. You need migration safety.

## The Problem: Locking Tables Under High Concurrency
PostgreSQL handles queries gracefully. It handles schema mutations under 15,000 requests per second brutally. A single unindexed foreign key check locks the parent table, cascading latency spikes across every microservice. 

Engineers try writing custom lock-timeout wrappers. These wrappers often fail silently or abandon half-applied DDL states that require manual rollbacks.

## How pg-teleport Fixes This
pg-teleport simulates your migration on an ephemeral, copy-on-write clone of your production database in 45 seconds. It catches lock contention before your CI/CD runner touches real customer data.

| Feature | What It Does | Why You Care |
| :--- | :--- | :--- |
| **Shadow Schema Staging** | Creates non-blocking shadow tables in background | Zero table locks during peak traffic |
| **Deterministic Dry-Run** | Replays recent query logs against migration clone | Verifies query plans before cutover |
| **Atomic Reversion** | Dual-write trigger rollback in under 200ms | If a query degrades, revert with zero data loss |

## Comparison: pg-teleport vs. Traditional Migrations

| Metric | Manual DDL / Flyway / Liquibase | pg-teleport |
| :--- | :--- | :--- |
| **Table Lock Duration** | Seconds to Minutes (Exclusive) | Zero (Atomic Pointer Switch) |
| **Pre-Flight Traffic Simulation** | None | Full 45-second replay |
| **Rollback Verification** | Manual & Risky | Automated & Instant |
| **Setup Overhead** | Hours of custom YAML scripts | Single standalone binary |

## Frequently Asked Questions

### Does pg-teleport require a dedicated daemon?
No. It ships as a single statically linked binary that runs directly inside your existing GitHub Actions, GitLab CI, or terminal.

### What versions of PostgreSQL are supported?
PostgreSQL 13, 14, 15, 16, and 17 on AWS Aurora, RDS, GCP Cloud SQL, and self-hosted Linux instances.

### Can it rollback data mutations after column deletion?
Yes. pg-teleport maintains an append-only transaction ledger during migration windows, allowing non-destructive rollbacks up to 48 hours post-deploy.

## Deploy in 3 Minutes
Stop sweating migrations. Download the CLI, run one pre-flight check, and push your schema updates with peace of mind.

```bash
curl -fsSL https://get.pg-teleport.dev | sh
pg-teleport verify ./migrations/2026_04_01_users.sql
```
