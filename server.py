from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json
from urllib.parse import urlparse, parse_qs, urlencode
import os
import sys
from datetime import datetime

class ProxyHandler(SimpleHTTPRequestHandler):
    def validate_dates(self, start_date, end_date):
        try:
            # Parse dates
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Validate date range
            if end < start:
                return False, "End date cannot be before start date"
            
            # Check if dates are not in the future
            if start > datetime.now() or end > datetime.now():
                return False, "Dates cannot be in the future"
            
            # Check if date range is not too large (e.g., max 1 year)
            if (end - start).days > 365:
                return False, "Date range cannot exceed 365 days"
            
            return True, None
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"

    def do_GET(self):
        print(f"Received request for path: {self.path}")
        
        if self.path == '/' or self.path == '':
            try:
                index_path = os.path.join(os.getcwd(), 'index.html')
                print(f"Attempting to serve: {index_path}")
                
                if not os.path.exists(index_path):
                    print(f"Error: {index_path} does not exist!")
                    self.send_error(404, "File not found")
                    return
                    
                with open(index_path, 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    print("Successfully served index.html")
                    return
            except Exception as e:
                print(f"Error serving index.html: {str(e)}")
                self.send_error(500, f"Internal server error: {str(e)}")
                return
        
        if self.path.startswith('/api/'):
            # Parse the URL and query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Validate required parameters
            if 'start_date' not in query_params or 'end_date' not in query_params:
                self.send_error(400, "Missing required parameters: start_date and end_date")
                return
            
            # Validate dates
            start_date = query_params['start_date'][0]
            end_date = query_params['end_date'][0]
            
            is_valid, error_message = self.validate_dates(start_date, end_date)
            if not is_valid:
                self.send_error(400, error_message)
                return
            
            # Reconstruct the API URL
            base_url = 'https://bossv2.bwesglobal.com' + parsed_url.path
            
            # Ensure single values for parameters
            cleaned_params = {k: v[0] for k, v in query_params.items()}
            
            # Construct the final URL with query parameters
            final_url = f"{base_url}?{urlencode(cleaned_params)}"
            
            try:
                print(f"Requesting API: {final_url}")
                req = urllib.request.Request(
                    final_url,
                    headers={
                        'User-Agent': 'Mozilla/5.0',
                        'Accept': 'application/json'
                    }
                )
                with urllib.request.urlopen(req) as response:
                    data = response.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(data)
                    print("API response received and sent to client")
            except Exception as e:
                print(f"API Error: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': str(e),
                    'url': final_url
                }).encode())
        else:
            # For all other paths, try to serve static files
            try:
                return SimpleHTTPRequestHandler.do_GET(self)
            except Exception as e:
                print(f"Error serving static file: {str(e)}")
                self.send_error(500, f"Internal server error: {str(e)}")

def run_server():
    try:
        # Change to the directory containing the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        print(f"Changed working directory to: {script_dir}")
        
        # Verify index.html exists
        if not os.path.exists('index.html'):
            print("Error: index.html not found in the current directory!")
            sys.exit(1)
            
        # Start the server
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, ProxyHandler)
        print('Starting server on port 8000...')
        print('Open http://localhost:8000 in your browser')
        print(f'Serving files from: {os.getcwd()}')
        httpd.serve_forever()
        
    except Exception as e:
        print(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run_server() 