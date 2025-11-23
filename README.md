# SPYDER Books Professional Connector

A professional MCP connector for Claude.ai that provides vector search across 278 AI/ML/Trading/Economics books.

## 🚀 Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/spyder-render-connector)

## Features

- 📚 Search 278 professional books
- 🔍 Vector similarity search using LanceDB
- 🌐 Professional HTTPS endpoint
- 🤖 Claude.ai MCP compatible
- ⚡ Fast response times

## Available Tools

### search_books
Search across all books using vector similarity.
```json
{
  "query": "machine learning techniques",
  "limit": 5
}
```

### get_stats
Get database statistics.
```json
{}
```

### list_categories  
List all book categories.
```json
{}
```

## Adding to Claude.ai

1. Go to Settings → Connectors
2. Click "Add Custom Connector"
3. Enter:
   - Name: `SPYDER Books`
   - URL: `https://your-app.onrender.com`
4. Click Add and Connect!

## Environment Variables

- `EC2_API_URL`: Your backend API URL (default: http://44.225.226.126:8571)

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

## Support

For issues or questions, please open a GitHub issue.
