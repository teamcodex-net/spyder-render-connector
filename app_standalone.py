"""
SPYDER Books Standalone Connector for Claude
Works without EC2 backend - includes sample book data
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import logging

app = Flask(__name__)
CORS(app)

# Sample book data (subset of your 278 books)
SAMPLE_BOOKS = [
    {
        "title": "Deep Learning",
        "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
        "category": "Machine Learning",
        "content": "Deep learning is a form of machine learning that enables computers to learn from experience and understand the world in terms of a hierarchy of concepts. This book introduces a broad range of topics in deep learning. The text offers mathematical and conceptual background, covering relevant concepts in linear algebra, probability theory and information theory, numerical computation, and machine learning.",
        "keywords": ["neural networks", "backpropagation", "optimization", "regularization", "convolutional networks", "recurrent networks", "deep generative models"]
    },
    {
        "title": "The Elements of Statistical Learning",
        "author": "Trevor Hastie, Robert Tibshirani, Jerome Friedman",
        "category": "Machine Learning",
        "content": "This book describes the important ideas in statistical learning - a vast and complex field. The book covers supervised learning, with topics including linear methods, kernel methods, model assessment and selection, boosting and additive trees, neural networks, support vector machines, and more.",
        "keywords": ["statistical learning", "data mining", "inference", "prediction", "supervised learning", "unsupervised learning"]
    },
    {
        "title": "Pattern Recognition and Machine Learning",
        "author": "Christopher Bishop",
        "category": "Machine Learning",
        "content": "This book presents approximate inference algorithms that permit fast approximate answers in situations where exact answers are not feasible. It covers Bayesian methods, graphical models, variational inference, sampling methods, and continuous latent variables.",
        "keywords": ["pattern recognition", "Bayesian methods", "graphical models", "neural networks", "kernel methods", "sampling methods"]
    },
    {
        "title": "Reinforcement Learning: An Introduction",
        "author": "Richard Sutton, Andrew Barto",
        "category": "Reinforcement Learning",
        "content": "Reinforcement learning is learning what to do - how to map situations to actions - so as to maximize a numerical reward signal. This book provides a clear and simple account of the key ideas and algorithms of reinforcement learning, including temporal-difference learning, Monte Carlo methods, and deep reinforcement learning.",
        "keywords": ["reinforcement learning", "Markov decision processes", "dynamic programming", "temporal-difference", "policy gradient", "deep RL"]
    },
    {
        "title": "Technical Analysis of the Financial Markets",
        "author": "John Murphy",
        "category": "Trading & Finance",
        "content": "This book covers the full spectrum of technical analysis applicable to financial markets. Topics include chart construction, basic concepts of trend, reversal patterns, continuation patterns, and computer trading systems.",
        "keywords": ["technical analysis", "chart patterns", "indicators", "trading systems", "market psychology", "Elliott wave"]
    },
    {
        "title": "Options, Futures, and Other Derivatives",
        "author": "John Hull",
        "category": "Trading & Finance", 
        "content": "The definitive guide to derivatives markets. This book covers mechanics of futures markets, hedging strategies, interest rates, determination of forward and futures prices, interest rate futures, swaps, options markets, trading strategies involving options, Black-Scholes-Merton model, and the Greek letters.",
        "keywords": ["derivatives", "options", "futures", "Black-Scholes", "hedging", "swaps", "risk management"]
    },
    {
        "title": "Advances in Financial Machine Learning",
        "author": "Marcos Lopez de Prado",
        "category": "Trading & Finance",
        "content": "This book addresses real-world problems faced by practitioners daily. It presents ML algorithms and techniques to address problems of backtesting, market microstructure, portfolio construction, and risk management. Topics include meta-labeling, fractionally differentiated features, and hierarchical risk parity.",
        "keywords": ["financial ML", "backtesting", "feature engineering", "portfolio optimization", "market microstructure", "meta-strategies"]
    },
    {
        "title": "Natural Language Processing with Python",
        "author": "Steven Bird, Ewan Klein, Edward Loper",
        "category": "Natural Language Processing",
        "content": "This book offers a practical introduction to programming for language processing. It covers categorizing and tagging words, analyzing sentence structure, building feature-based grammars, analyzing the meaning of sentences, and managing linguistic data.",
        "keywords": ["NLP", "NLTK", "tokenization", "parsing", "semantic analysis", "corpus linguistics"]
    },
    {
        "title": "Hands-On Machine Learning",
        "author": "Aurélien Géron",
        "category": "Machine Learning",
        "content": "This practical book shows you how to build intelligent systems using Scikit-Learn, Keras, and TensorFlow. Topics include linear regression, classification, training models, support vector machines, decision trees, ensemble learning, and deep neural networks.",
        "keywords": ["scikit-learn", "TensorFlow", "Keras", "practical ML", "deep learning", "neural networks"]
    },
    {
        "title": "The Intelligent Investor",
        "author": "Benjamin Graham",
        "category": "Trading & Finance",
        "content": "The classic text on value investing. This book describes the philosophy of value investing which shields investors from substantial error and teaches them to develop long-term strategies. Topics include investment versus speculation, the investor and market fluctuations, margin of safety, and security analysis.",
        "keywords": ["value investing", "fundamental analysis", "margin of safety", "Mr. Market", "defensive investing", "enterprising investing"]
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SPYDER Books Connector</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 20px;
        }
        .status { 
            text-align: center;
            padding: 10px 20px;
            background: #10b981;
            color: white;
            border-radius: 20px;
            display: inline-block;
            margin: 0 auto 30px;
            width: 100%;
        }
        .info {
            background: #f8fafc;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat {
            text-align: center;
            padding: 20px;
            background: #f1f5f9;
            border-radius: 12px;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }
        .instructions {
            background: #fef3c7;
            border: 2px solid #fbbf24;
            border-radius: 12px;
            padding: 20px;
            margin-top: 30px;
        }
        code {
            background: #1e293b;
            color: #10b981;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 SPYDER Books</h1>
        <div class="status">✅ Connector Active (Standalone Mode)</div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">278</div>
                <div>Books</div>
            </div>
            <div class="stat">
                <div class="stat-value">10</div>
                <div>Sample Books</div>
            </div>
            <div class="stat">
                <div class="stat-value">Active</div>
                <div>Status</div>
            </div>
        </div>
        
        <div class="info">
            <h3>🔌 MCP Endpoint</h3>
            <p style="margin-top: 10px;"><code>{{ request.url_root }}</code></p>
        </div>
        
        <div class="instructions">
            <h3>📱 Add to Claude.ai:</h3>
            <ol style="margin-top: 15px; padding-left: 20px;">
                <li>Settings → Connectors</li>
                <li>Add Custom Connector</li>
                <li>Name: <strong>SPYDER Books</strong></li>
                <li>URL: <strong>{{ request.url_root }}</strong></li>
                <li>Connect!</li>
            </ol>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'SPYDER Books Connector',
        'version': '3.0.0',
        'mode': 'standalone'
    })

@app.route('/mcp')
@app.route('/mcp/')
def mcp_info():
    return jsonify({
        'name': 'SPYDER Books Connector',
        'version': '3.0.0',
        'mcp_version': '2024-11-05',
        'description': '278 AI/ML/Trading books (sample data)',
        'capabilities': {
            'tools': ['search_books', 'get_stats', 'list_categories']
        }
    })

@app.route('/mcp/tools/list', methods=['GET', 'POST'])
def list_tools():
    return jsonify({
        'tools': [
            {
                'name': 'search_books',
                'description': 'Search books by content or topic',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'query': {'type': 'string'},
                        'limit': {'type': 'integer', 'default': 5}
                    },
                    'required': ['query']
                }
            },
            {
                'name': 'get_stats',
                'description': 'Get database statistics',
                'inputSchema': {'type': 'object', 'properties': {}}
            },
            {
                'name': 'list_categories',
                'description': 'List book categories',
                'inputSchema': {'type': 'object', 'properties': {}}
            }
        ]
    })

@app.route('/mcp/tools/call', methods=['POST'])
def call_tool():
    data = request.json or {}
    tool_name = data.get('name')
    arguments = data.get('arguments', {})
    
    if tool_name == 'search_books':
        query = arguments.get('query', '').lower()
        limit = min(arguments.get('limit', 5), 10)
        
        # Search through sample books
        results = []
        for book in SAMPLE_BOOKS:
            score = 0
            query_words = query.split()
            
            # Search in all fields
            searchable_text = f"{book['title']} {book['author']} {book['category']} {book['content']} {' '.join(book['keywords'])}".lower()
            
            for word in query_words:
                if word in searchable_text:
                    score += searchable_text.count(word)
            
            if score > 0:
                results.append({
                    'title': book['title'],
                    'author': book['author'],
                    'category': book['category'],
                    'content': book['content'][:300] + '...',
                    'score': score,
                    'keywords': book['keywords'][:5]
                })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        results = results[:limit]
        
        output = {
            'query': arguments.get('query', ''),
            'results': results,
            'count': len(results),
            'total_books': 278,
            'note': 'Showing sample books. Full database has 278 books.'
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
                    'sample_books_available': len(SAMPLE_BOOKS),
                    'categories': ['Machine Learning', 'Deep Learning', 'Trading & Finance', 'NLP', 'Reinforcement Learning'],
                    'mode': 'standalone',
                    'status': 'active'
                })
            }
        })
    
    elif tool_name == 'list_categories':
        categories = list(set([book['category'] for book in SAMPLE_BOOKS]))
        return jsonify({
            'tool_result': {
                'output': json.dumps({
                    'categories': categories,
                    'total': len(categories),
                    'note': 'Full database has more categories'
                })
            }
        })
    
    else:
        return jsonify({'error': f'Unknown tool: {tool_name}'}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    port = 5000
    print(f"Starting SPYDER Books Connector on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
