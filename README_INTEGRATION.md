# README

## New features
- **Export Bundle (.zip)** button packages the latest KPI CSV, Parent CSV, and Suggestions JSON for quick sharing.
- **Webhook toggle** can POST suggestions to your SportsKey endpoint (set the URL in the UI or via env `SPORTSKEY_WEBHOOK_URL`).

### Suggested webhook payload
```json
{
  "source": "SportAI.RevPAH",
  "generated_at": "2025-10-27T15:00:00Z",
  "suggestions": [ { "asset": "HalfTurf-A", "from_hour": "...", "to_hour": "...", "reason": "..." } ]
}
```
