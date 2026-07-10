<div align=center>
  <h1>✅ EEAT Analyzer</h1>
  <p><em>Scores any URL for EEAT signals: named author, credentials, publish dates, external references, schema markup. 0-100.</em></p>
  <p><a href=LICENSE><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt=License></a>
  <a href=https://github.com/josezuma/eeat-analyzer/actions/workflows/ci.yml><img src="https://img.shields.io/badge/CI-passing-green.svg"></a></p>
  <p>by <a href=https://brandvirality.com>BrandVirality</a><br>
  <strong>Author:</strong> <a href=https://github.com/josezuma>Jose Zuma — Expert in AI Visibility</a></p>
</div>

---

## Quick Start

```bash
pip install requests beautifulsoup4
python3 scripts/analyze.py https://example.com
```

## Scoring (100 pts)

| Signal | Points | What it checks |
|--------|:------:|----------------|
| Named author | 25 | Real name in byline or schema |
| Author credentials | 20 | Bio, job title, LinkedIn, expertise |
| Publish date | 20 | Visible date + datePublished schema |
| External references | 20 | Links to sources, citations |
| Schema.org markup | 15 | Article, Person, Organization schema |

## Related
geo-audit-skill, schema-for-ai, awesome-ai-visibility, mcp-geo
