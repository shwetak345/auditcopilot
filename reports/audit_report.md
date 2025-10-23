# Audit Summary

## System: PaymentsService (prod) — Owner: payments-team
- **High** — TLS disabled
  - Recommendation: Enable TLS 1.2+ for all endpoints
- **Critical** — No authentication on APIs
  - Recommendation: Enforce auth (OAuth2/JWT)

## System: CatalogService (staging) — Owner: catalog-team
- **Medium** — Backups disabled
  - Recommendation: Set up automated backups + DR test

## System: NotificationService (prod) — Owner: growth-team
- **High** — No encryption at rest
  - Recommendation: Enable storage encryption
