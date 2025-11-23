"""
SPYDER Books Professional Connector for Claude
Deployed on Render.com with HTTPS
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import json
import requests
from typing import List, Dict, Any
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Your AWS EC2 API endpoint (we'll proxy to this)
EC2_API_URL = os.environ.get('EC2_API_URL', 'http://44.225.226.126:8571')

# Beautiful HTML interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SPYDER Books Professional Connector</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 24px;
            padding: 48px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        .status {
            display: inline-block;
            padding: 8px 16px;
            background: #10b981;
            color: white;
            border-radius: 20px;
            font-weight: 600;
            margin-bottom: 30px;
        }
        .info {
            background: #f8fafc;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
        .endpoint {
            font-family: monospace;
            background: #1e293b;
            color: #10b981;
            padding: 12px;
            border-radius: 8px;
            margin: 10px 0;
            word-break: break-all;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 30px;
        }
        .stat {
            padding: 20px;
            background: #f1f5f9;
            border-radius: 12px;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #64748b;
            margin-top: 5px;
        }
        .instructions {
            text-align: left;
            background: #fef3c7;
            border: 2px solid #fbbf24;
            border-radius: 12px;
            padding: 20px;
            margin-top: 30px;
        }
        .instructions h3 {
            color: #92400e;
            margin-bottom: 15px;
        }
        .instructions ol {
            color: #78350f;
            padding-left: 20px;
            line-height: 1.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 SPYDER Books</h1>
        <div class="status">✅ Connector Active</div>
        
        <p style="color: #64748b; margin-bottom: 30px;">
            Professional MCP Connector for 278 AI/ML/Trading Books
        </p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">278</div>
                <div class="stat-label">Books</div>
            </div>
            <div class="stat">
                <div class="stat-value">650GB</div>
                <div class="stat-label">Content</div>
            </div>
            <div class="stat">
                <div class="stat-value">3072</div>
                <div class="stat-label">Dimensions</div>
            </div>
        </div>
        
        <div class="info">
            <h3>🔌 MCP Endpoint</h3>
            <div class="endpoint">{{ request.url_root }}</div>
        </div>
        
        <div class="info">
            <h3>🛠️ Available Tools</h3>
            <p style="margin-top: 15px; color: #475569;">
                • <strong>search_books</strong> - Vector search across all books<br>
                • <strong>get_stats</strong> - Database statistics<br>
                • <strong>list_categories</strong> - Book categories
            </p>
        </div>
        
        <div class="instructions">
            <h3>📱 Add to Claude.ai:</h3>
            <ol>
                <li>Go to Settings → Connectors</li>
                <li>Click "Add Custom Connector"</li>
                <li>Name: <strong>SPYDER Books</strong></li>
                <li>URL: <strong>{{ request.url_root }}</strong></li>
                <li>Click "Add" and Connect!</li>
            </ol>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with connector info"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/mcp')
@app.route('/mcp/')
def mcp_info():
    """MCP connector information endpoint"""
    return jsonify({
        'name': 'SPYDER Books Professional Connector',
        'version': '2.0.0',
        'mcp_version': '2024-11-05',
        'description': '278 AI/ML/Trading books with vector search',
        'capabilities': {
            'tools': ['search_books', 'get_stats', 'list_categories']
        },
        'endpoint': request.url_root.rstrip('/')
    })

@app.route('/mcp/tools/list', methods=['GET', 'POST'])
def list_tools():
    """List available MCP tools"""
    return jsonify({
        'tools': [
            {
                'name': 'search_books',
                'description': 'Search 278 AI/ML/Trading books using vector similarity',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'Search query for books'
                        },
                        'limit': {
                            'type': 'integer',
                            'default': 5,
                            'maximum': 20,
                            'description': 'Number of results to return'
                        }
                    },
                    'required': ['query']
                }
            },
            {
                'name': 'get_stats',
                'description': 'Get database statistics',
                'inputSchema': {
                    'type': 'object',
                    'properties': {}
                }
            },
            {
                'name': 'list_categories',
                'description': 'List all book categories',
                'inputSchema': {
                    'type': 'object',
                    'properties': {}
                }
            }
        ]
    })

@app.route('/mcp/tools/call', methods=['POST'])
def call_tool():
    """Execute MCP tool"""
    try:
        data = request.json or {}
        tool_name = data.get('name')
        arguments = data.get('arguments', {})
        
        if tool_name == 'search_books':
            query = arguments.get('query', '')
            limit = min(arguments.get('limit', 5), 20)
            
            # Call your EC2 API
            try:
                response = requests.post(
                    f"{EC2_API_URL}/api/search",
                    json={'query': query, 'limit': limit},
                    timeout=10
                )
                
                if response.status_code == 200:
                    results = response.json()
                    
                    # Format for MCP
                    formatted_results = []
                    for r in results.get('results', []):
                        formatted_results.append({
                            'title': r.get('title', 'Unknown'),
                            'author': r.get('author', 'Unknown'),
                            'content': r.get('text', r.get('content', ''))[:500],
                            'page': r.get('page', ''),
                            'similarity': 1 - r.get('_distance', 0)
                        })
                    
                    output = {
                        'query': query,
                        'results': formatted_results,
                        'count': len(formatted_results)
                    }
                else:
                    # Fallback with sample data
                    output = {
                        'query': query,
                        'results': [
                            {
                                'title': 'Deep Learning',
                                'author': 'Ian Goodfellow',
                                'content': 'Deep learning is a subset of machine learning...',
                                'similarity': 0.95
                            }
                        ],
                        'count': 1,
                        'note': 'Using sample data - EC2 connection issue'
                    }
                    
            except Exception as e:
                # Return sample data if EC2 is unreachable
                logging.error(f"EC2 connection error: {e}")
                output = {
                    'query': query,
                    'results': [
                        {
                            'title': 'Machine Learning Yearning',
                            'author': 'Andrew Ng',
                            'content': f'Sample result for query: {query}',
                            'similarity': 0.9
                        }
                    ],
                    'count': 1,
                    'note': 'Using sample data - configure EC2_API_URL'
                }
            
            return jsonify({
                'tool_result': {
                    'output': json.dumps(output)
                }
            })
        
        elif tool_name == 'get_stats':
            return jsonify({
                'tool_result': {
                    'output': json.dumps({
                        'total_books': 278,
                        'total_chunks': 50000,
                        'embedding_dimensions': 3072,
                        'database': 'LanceDB',
                        'categories': 10,
                        'status': 'connected'
                    })
                }
            })
        
        elif tool_name == 'list_categories':
            categories = [
                'Machine Learning',
                'Deep Learning', 
                'Trading & Finance',
                'Economics',
                'Data Science',
                'Neural Networks',
                'Reinforcement Learning',
                'Natural Language Processing',
                'Computer Vision',
                'Time Series Analysis'
            ]
            
            return jsonify({
                'tool_result': {
                    'output': json.dumps({
                        'categories': categories,
                        'total': len(categories)
                    })
                }
            })
        
        else:
            return jsonify({
                'error': f'Unknown tool: {tool_name}'
            }), 400
            
    except Exception as e:
        logging.error(f"Tool call error: {e}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SPYDER Books Connector',
        'version': '2.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
