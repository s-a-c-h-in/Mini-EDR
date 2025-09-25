from flask import Flask, render_template, jsonify
import json
from database.manager import DatabaseManager

app = Flask(__name__)
db = DatabaseManager()

@app.route('/')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mini EDR Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background: #2c3e50; color: white; padding: 20px; }
            .stats { display: flex; gap: 20px; margin: 20px 0; }
            .stat-card { background: #ecf0f1; padding: 20px; border-radius: 5px; }
            .alert { background: #e74c3c; color: white; padding: 10px; margin: 5px 0; }
            .event { background: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 3px solid #3498db; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🛡️ Mini EDR Dashboard</h1>
            <p>Protection Status: <span style="color: #2ecc71;">✅ ACTIVE</span></p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>System Health</h3>
                <p>CPU: 15%</p>
                <p>Memory: 45%</p>
                <p>Processes: 156</p>
            </div>
            
            <div class="stat-card">
                <h3>Monitoring Stats</h3>
                <p>Files Monitored: 45,672</p>
                <p>Events Today: 234</p>
                <p>Threats Blocked: 3</p>
            </div>
        </div>
        
        <h2>Recent Alerts</h2>
        <div id="alerts"></div>
        
        <h2>Recent Events</h2>
        <div id="events"></div>
        
        <script>
            function loadData() {
                fetch('/api/events')
                    .then(response => response.json())
                    .then(data => {
                        const eventsDiv = document.getElementById('events');
                        eventsDiv.innerHTML = '';
                        data.forEach(event => {
                            const eventData = JSON.parse(event[3]);
                            const div = document.createElement('div');
                            div.className = event[4] === 'high' ? 'alert' : 'event';
                            div.innerHTML = `
                                <strong>${event[2]}</strong> - ${event[1]}<br>
                                Risk: ${event[4]} | Details: ${JSON.stringify(eventData).substring(0, 100)}...
                            `;
                            eventsDiv.appendChild(div);
                        });
                    });
            }
            
            setInterval(loadData, 5000);
            loadData();
        </script>
    </body>
    </html>
    '''

@app.route('/api/events')
def api_events():
    events = db.get_recent_events(50)
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
