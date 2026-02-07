---
name: ddgr-search
description: Search the web using ddgr (DuckDuckGo CLI). Use when you need to find information on the web using a privacy-focused search engine.
---

# ddgr Search Skill

This skill allows you to search the web using `ddgr`.

## Usage

### Basic Search
To perform a basic search and get JSON output (best for AI processing):
```bash
ddgr --json -n 5 "your search query"
```

### Options
- `-n N`: Number of results (default 10, max 25).
- `-r REG`: Region-specific search (e.g., `jp-jp` for Japan, `us-en` for US).
- `-t SPAN`: Time limit (`d` for day, `w` for week, `m` for month, `y` for year).
- `-w SITE`: Search within a specific site.

### Examples

**Search for news about OpenClaw in the last week (Japan region):**
```bash
ddgr --json -n 3 -r jp-jp -t w "OpenClaw"
```

**Search for Python tutorials on StackOverflow:**
```bash
ddgr --json -w stackoverflow.com "python tutorial"
```

## Tips
- Always use `--json` when you want to parse the results programmatically.
- Combine with `web_fetch` or `browser` to read the actual content of the search results.
