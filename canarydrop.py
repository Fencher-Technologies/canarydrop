#!/usr/bin/env python3
"""
CanaryDrop CLI - Create and manage canary tokens for security monitoring
A lightweight security tool for detecting unauthorized access
"""

import json
import os
import sqlite3
import secrets
import hashlib
from datetime import datetime
from pathlib import Path
import argparse
import sys

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colored(text, color):
    """Return colored text for terminal"""
    return f"{color}{text}{Colors.ENDC}"

# Configuration
CONFIG_DIR = Path.home() / ".canarydrop"
DB_PATH = CONFIG_DIR / "canaries.db"

class CanaryDB:
    """Database manager for canary tokens"""
    
    def __init__(self):
        CONFIG_DIR.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS canaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_id TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                memo TEXT,
                alert_method TEXT,
                alert_destination TEXT,
                created_at TEXT NOT NULL,
                accessed_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                metadata TEXT
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_id TEXT NOT NULL,
                accessed_at TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                metadata TEXT,
                FOREIGN KEY (token_id) REFERENCES canaries(token_id)
            )
        """)
        self.conn.commit()
    
    def create_canary(self, canary_data):
        """Insert new canary token"""
        self.conn.execute("""
            INSERT INTO canaries 
            (token_id, type, name, memo, alert_method, alert_destination, created_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            canary_data['token_id'],
            canary_data['type'],
            canary_data['name'],
            canary_data.get('memo', ''),
            canary_data.get('alert_method', 'console'),
            canary_data.get('alert_destination', ''),
            canary_data['created_at'],
            json.dumps(canary_data.get('metadata', {}))
        ))
        self.conn.commit()
    
    def list_canaries(self, token_type=None):
        """List all canaries, optionally filtered by type"""
        query = "SELECT * FROM canaries"
        params = []
        
        if token_type:
            query += " WHERE type = ?"
            params.append(token_type)
        
        query += " ORDER BY created_at DESC"
        
        cursor = self.conn.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_canary(self, token_id):
        """Get specific canary by token_id"""
        cursor = self.conn.execute(
            "SELECT * FROM canaries WHERE token_id = ?", 
            (token_id,)
        )
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else None
    
    def delete_canary(self, token_id):
        """Delete a canary token"""
        self.conn.execute("DELETE FROM access_logs WHERE token_id = ?", (token_id,))
        self.conn.execute("DELETE FROM canaries WHERE token_id = ?", (token_id,))
        self.conn.commit()
    
    def log_access(self, token_id, ip_address=None, user_agent=None, metadata=None):
        """Log an access attempt to a canary"""
        # Update canary access count
        self.conn.execute("""
            UPDATE canaries 
            SET accessed_count = accessed_count + 1,
                last_accessed = ?
            WHERE token_id = ?
        """, (datetime.now().isoformat(), token_id))
        
        # Insert access log
        self.conn.execute("""
            INSERT INTO access_logs 
            (token_id, accessed_at, ip_address, user_agent, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            token_id,
            datetime.now().isoformat(),
            ip_address,
            user_agent,
            json.dumps(metadata or {})
        ))
        self.conn.commit()
    
    def get_access_logs(self, token_id=None, limit=100):
        """Get access logs, optionally filtered by token_id"""
        query = "SELECT * FROM access_logs"
        params = []
        
        if token_id:
            query += " WHERE token_id = ?"
            params.append(token_id)
        
        query += " ORDER BY accessed_at DESC LIMIT ?"
        params.append(limit)
        
        cursor = self.conn.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection"""
        self.conn.close()


class CanaryGenerator:
    """Generate different types of canary tokens"""
    
    @staticmethod
    def generate_token_id(prefix=""):
        """Generate unique token ID"""
        random_part = secrets.token_hex(16)
        if prefix:
            return f"{prefix}_{random_part}"
        return random_part
    
    @staticmethod
    def generate_dns_token(name):
        """Generate DNS canary token"""
        token_id = CanaryGenerator.generate_token_id("dns")
        hostname = f"{token_id}.canarytokens.local"
        
        return {
            'token_id': token_id,
            'type': 'dns',
            'name': name,
            'hostname': hostname,
            'metadata': {
                'hostname': hostname,
                'record_type': 'A'
            }
        }
    
    @staticmethod
    def generate_http_token(name):
        """Generate HTTP canary token"""
        token_id = CanaryGenerator.generate_token_id("http")
        url = f"https://canarytokens.local/{token_id}"
        
        return {
            'token_id': token_id,
            'type': 'http',
            'name': name,
            'url': url,
            'metadata': {
                'url': url,
                'method': 'GET'
            }
        }
    
    @staticmethod
    def generate_aws_key(name):
        """Generate fake AWS credentials"""
        token_id = CanaryGenerator.generate_token_id("aws")
        
        # Generate fake but realistic looking AWS credentials
        access_key = "AKIA" + secrets.token_hex(10).upper()
        secret_key = secrets.token_urlsafe(30)
        
        return {
            'token_id': token_id,
            'type': 'aws-key',
            'name': name,
            'access_key': access_key,
            'secret_key': secret_key,
            'metadata': {
                'access_key_id': access_key,
                'secret_access_key': secret_key,
                'region': 'us-east-1'
            }
        }
    
    @staticmethod
    def generate_sql_token(name):
        """Generate fake SQL connection string"""
        token_id = CanaryGenerator.generate_token_id("sql")
        
        username = f"canary_{secrets.token_hex(4)}"
        password = secrets.token_urlsafe(16)
        host = f"db-{secrets.token_hex(4)}.canarytokens.local"
        database = name.lower().replace(" ", "_")
        
        connection_string = f"mysql://{username}:{password}@{host}:3306/{database}"
        
        return {
            'token_id': token_id,
            'type': 'sql',
            'name': name,
            'connection_string': connection_string,
            'metadata': {
                'host': host,
                'username': username,
                'password': password,
                'database': database,
                'port': 3306,
                'type': 'mysql'
            }
        }
    
    @staticmethod
    def generate_email_token(name):
        """Generate email canary token"""
        token_id = CanaryGenerator.generate_token_id("email")
        email = f"{token_id}@canarytokens.local"
        
        return {
            'token_id': token_id,
            'type': 'email',
            'name': name,
            'email': email,
            'metadata': {
                'email': email
            }
        }
    
    @staticmethod
    def generate_api_key(name):
        """Generate fake API key"""
        token_id = CanaryGenerator.generate_token_id("api")
        
        api_key = f"sk_{secrets.token_urlsafe(32)}"
        
        return {
            'token_id': token_id,
            'type': 'api-key',
            'name': name,
            'api_key': api_key,
            'metadata': {
                'api_key': api_key,
                'key_type': 'secret_key'
            }
        }
    
    @staticmethod
    def generate_qr_code(name, url=None):
        """Generate QR code canary token"""
        token_id = CanaryGenerator.generate_token_id("qr")
        
        if not url:
            url = f"https://canarytokens.local/qr/{token_id}"
        
        return {
            'token_id': token_id,
            'type': 'qr-code',
            'name': name,
            'url': url,
            'metadata': {
                'url': url,
                'format': 'url',
                'note': 'Use online QR generator with this URL'
            }
        }
    
    @staticmethod
    def generate_document_token(name, doc_type='docx'):
        """Generate document with embedded canary"""
        token_id = CanaryGenerator.generate_token_id("doc")
        callback_url = f"https://canarytokens.local/doc/{token_id}/track.gif"
        
        return {
            'token_id': token_id,
            'type': f'document-{doc_type}',
            'name': name,
            'callback_url': callback_url,
            'metadata': {
                'document_type': doc_type,
                'callback_url': callback_url,
                'tracking_pixel': True
            }
        }


def cmd_create(args):
    """Create a new canary token"""
    db = CanaryDB()
    
    try:
        # Generate the appropriate canary type
        token_type = args.type
        name = args.name
        
        if token_type == 'dns':
            canary = CanaryGenerator.generate_dns_token(name)
        elif token_type == 'http':
            canary = CanaryGenerator.generate_http_token(name)
        elif token_type == 'aws-key':
            canary = CanaryGenerator.generate_aws_key(name)
        elif token_type == 'sql':
            canary = CanaryGenerator.generate_sql_token(name)
        elif token_type == 'email':
            canary = CanaryGenerator.generate_email_token(name)
        elif token_type == 'api-key':
            canary = CanaryGenerator.generate_api_key(name)
        elif token_type == 'qr-code':
            canary = CanaryGenerator.generate_qr_code(name, args.url)
        elif token_type == 'document':
            canary = CanaryGenerator.generate_document_token(name)
        else:
            print(colored(f"✗ Invalid token type: {token_type}", Colors.RED))
            return
        
        # Add common fields
        canary['memo'] = args.memo or ''
        canary['alert_method'] = args.alert or 'console'
        canary['alert_destination'] = args.destination or ''
        canary['created_at'] = datetime.now().isoformat()
        
        # Save to database
        db.create_canary(canary)
        
        print(colored("\n✓ Canary token created successfully!", Colors.GREEN + Colors.BOLD))
        print(f"\nToken ID: {colored(canary['token_id'], Colors.CYAN + Colors.BOLD)}")
        print(f"Type: {token_type}")
        print(f"Name: {name}")
        
        # Display type-specific information
        if token_type == 'dns':
            print(f"\nHostname: {colored(canary['hostname'], Colors.YELLOW)}")
            print("\nUsage: Embed this hostname in configs or scripts")
            
        elif token_type == 'http':
            print(f"\nURL: {colored(canary['url'], Colors.YELLOW)}")
            print("\nUsage: Share this URL or embed in web pages")
            
        elif token_type == 'aws-key':
            print(f"\nAccess Key ID: {colored(canary['access_key'], Colors.YELLOW)}")
            print(f"Secret Access Key: {colored(canary['secret_key'], Colors.YELLOW)}")
            print("\nUsage: Plant in config files, .env files, or scripts")
            print("\nExample AWS config:")
            print(f"  [profile {name}]")
            print(f"  aws_access_key_id = {canary['access_key']}")
            print(f"  aws_secret_access_key = {canary['secret_key']}")
            print(f"  region = us-east-1")
            
        elif token_type == 'sql':
            print(f"\nConnection String: {colored(canary['connection_string'], Colors.YELLOW)}")
            print("\nUsage: Plant in application configs or .env files")
            print("\nExample .env entry:")
            print(f"  DATABASE_URL={canary['connection_string']}")
            
        elif token_type == 'email':
            print(f"\nEmail: {colored(canary['email'], Colors.YELLOW)}")
            print("\nUsage: Use as contact email in documents or configs")
            
        elif token_type == 'api-key':
            print(f"\nAPI Key: {colored(canary['api_key'], Colors.YELLOW)}")
            print("\nUsage: Plant in scripts or configuration files")
            
        elif token_type == 'qr-code':
            print(f"\nURL: {colored(canary['url'], Colors.YELLOW)}")
            print("\nTo create QR code:")
            print(f"  Visit: https://www.qr-code-generator.com/")
            print(f"  Enter URL: {canary['url']}")
            
        elif token_type == 'document':
            print(f"\nCallback URL: {colored(canary['callback_url'], Colors.YELLOW)}")
            print("\nUsage: Create a document and embed this URL as a hidden image")
        
        print(f"\n{colored('⚠', Colors.RED)}  Monitor with: python canarydrop.py history --token {canary['token_id']}")
        
    except Exception as e:
        print(colored(f"\n✗ Error creating canary: {str(e)}", Colors.RED))
    finally:
        db.close()


def cmd_list(args):
    """List all canary tokens"""
    db = CanaryDB()
    
    try:
        canaries = db.list_canaries(args.type)
        
        if not canaries:
            print("No canary tokens found.")
            return
        
        if args.json:
            print(json.dumps(canaries, indent=2))
        else:
            print(colored(f"\n{'='*80}", Colors.CYAN))
            print(colored(f"{'CANARY TOKENS':^80}", Colors.CYAN + Colors.BOLD))
            print(colored(f"{'='*80}", Colors.CYAN))
            
            for canary in canaries:
                status = "🔴 TRIGGERED" if canary['accessed_count'] > 0 else "🟢 ACTIVE"
                
                print(f"\n{status} | {colored(canary['type'].upper(), Colors.YELLOW + Colors.BOLD)}")
                print(f"Name: {canary['name']}")
                print(f"Token ID: {colored(canary['token_id'], Colors.CYAN)}")
                print(f"Created: {canary['created_at'][:19]}")
                
                if canary['accessed_count'] > 0:
                    print(colored(f"⚠ Accessed: {canary['accessed_count']} times", Colors.RED))
                    print(f"Last access: {canary['last_accessed'][:19]}")
                
                if canary['memo']:
                    print(f"Memo: {canary['memo']}")
                
                print(colored(f"{'-'*80}", Colors.BLUE))
            
            print(f"\nTotal: {len(canaries)} canaries")
            
    finally:
        db.close()


def cmd_history(args):
    """Show access history for canary tokens"""
    db = CanaryDB()
    
    try:
        logs = db.get_access_logs(args.token, args.limit)
        
        if not logs:
            if args.token:
                canary = db.get_canary(args.token)
                if canary:
                    print(colored(f"\n✓ Token '{args.token}' exists but has not been accessed yet.", Colors.GREEN))
                else:
                    print(colored(f"\n✗ Token '{args.token}' not found.", Colors.RED))
            else:
                print("No access logs found.")
            return
        
        if args.json:
            print(json.dumps(logs, indent=2))
        else:
            print(colored(f"\n{'='*80}", Colors.RED))
            print(colored(f"{'CANARY ACCESS LOGS':^80}", Colors.RED + Colors.BOLD))
            print(colored(f"{'='*80}", Colors.RED))
            
            for log in logs:
                canary = db.get_canary(log['token_id'])
                
                print(f"\n🚨 {colored('ALERT', Colors.RED + Colors.BOLD)} - {log['accessed_at'][:19]}")
                print(f"Token: {colored(log['token_id'], Colors.CYAN)}")
                
                if canary:
                    print(f"Name: {canary['name']}")
                    print(f"Type: {canary['type']}")
                
                if log['ip_address']:
                    print(f"IP Address: {log['ip_address']}")
                if log['user_agent']:
                    print(f"User Agent: {log['user_agent']}")
                
                if log['metadata'] and log['metadata'] != '{}':
                    metadata = json.loads(log['metadata'])
                    print("Additional Info:")
                    for key, value in metadata.items():
                        print(f"  {key}: {value}")
                
                print(colored(f"{'-'*80}", Colors.BLUE))
            
            print(f"\nTotal: {len(logs)} access events")
            
    finally:
        db.close()


def cmd_delete(args):
    """Delete a canary token"""
    db = CanaryDB()
    
    try:
        canary = db.get_canary(args.token_id)
        
        if not canary:
            print(colored(f"\n✗ Token '{args.token_id}' not found.", Colors.RED))
            return
        
        if not args.yes:
            response = input(f"Delete canary '{canary['name']}'? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Cancelled.")
                return
        
        db.delete_canary(args.token_id)
        print(colored(f"\n✓ Canary token '{canary['name']}' deleted successfully.", Colors.GREEN))
        
    finally:
        db.close()


def cmd_info(args):
    """Show detailed information about a canary token"""
    db = CanaryDB()
    
    try:
        canary = db.get_canary(args.token_id)
        
        if not canary:
            print(colored(f"\n✗ Token '{args.token_id}' not found.", Colors.RED))
            return
        
        status = "🔴 TRIGGERED" if canary['accessed_count'] > 0 else "🟢 ACTIVE"
        
        print(colored(f"\n{'='*80}", Colors.CYAN))
        print(colored(f"{status} CANARY TOKEN DETAILS", Colors.CYAN + Colors.BOLD))
        print(colored(f"{'='*80}", Colors.CYAN))
        
        print(f"\nToken ID: {colored(canary['token_id'], Colors.CYAN + Colors.BOLD)}")
        print(f"Type: {canary['type']}")
        print(f"Name: {canary['name']}")
        print(f"Created: {canary['created_at'][:19]}")
        
        if canary['memo']:
            print(f"Memo: {canary['memo']}")
        
        print(f"\nAlert Method: {canary['alert_method']}")
        if canary['alert_destination']:
            print(f"Alert Destination: {canary['alert_destination']}")
        
        print(f"\nAccess Count: {canary['accessed_count']}")
        if canary['last_accessed']:
            print(f"Last Accessed: {canary['last_accessed'][:19]}")
        
        if canary['metadata']:
            metadata = json.loads(canary['metadata'])
            print(f"\n{colored('Token-Specific Data:', Colors.BOLD)}")
            for key, value in metadata.items():
                print(f"  {key}: {colored(str(value), Colors.YELLOW)}")
        
    finally:
        db.close()


def cmd_trigger(args):
    """Manually trigger a canary token"""
    db = CanaryDB()
    
    try:
        canary = db.get_canary(args.token_id)
        
        if not canary:
            print(colored(f"\n✗ Token '{args.token_id}' not found.", Colors.RED))
            return
        
        meta_dict = {}
        if args.metadata:
            try:
                meta_dict = json.loads(args.metadata)
            except json.JSONDecodeError:
                print(colored("Warning: Invalid JSON metadata, ignoring.", Colors.YELLOW))
        
        db.log_access(args.token_id, args.ip, args.user_agent, meta_dict)
        
        print(colored(f"\n🚨 Canary token triggered!", Colors.RED + Colors.BOLD))
        print(f"Token: {canary['name']} ({args.token_id})")
        print(f"Time: {datetime.now().isoformat()}")
        
        if args.ip:
            print(f"IP: {args.ip}")
        if args.user_agent:
            print(f"User Agent: {args.user_agent}")
        
        # Simulate alert
        if canary['alert_method'] == 'console':
            print(colored(f"\n⚠ Alert sent to console", Colors.YELLOW))
        elif canary['alert_method'] == 'email' and canary['alert_destination']:
            print(colored(f"\n⚠ Alert would be sent to: {canary['alert_destination']}", Colors.YELLOW))
        elif canary['alert_method'] == 'webhook' and canary['alert_destination']:
            print(colored(f"\n⚠ Alert would be sent to webhook: {canary['alert_destination']}", Colors.YELLOW))
        
    finally:
        db.close()


def cmd_stats(args):
    """Show statistics about canary tokens"""
    db = CanaryDB()
    
    try:
        canaries = db.list_canaries()
        logs = db.get_access_logs(limit=1000)
        
        total = len(canaries)
        triggered = len([c for c in canaries if c['accessed_count'] > 0])
        active = total - triggered
        
        type_counts = {}
        for canary in canaries:
            type_counts[canary['type']] = type_counts.get(canary['type'], 0) + 1
        
        print(colored(f"\n{'='*80}", Colors.CYAN))
        print(colored(f"{'CANARY TOKEN STATISTICS':^80}", Colors.CYAN + Colors.BOLD))
        print(colored(f"{'='*80}", Colors.CYAN))
        
        print(f"\nTotal Canaries: {colored(str(total), Colors.CYAN + Colors.BOLD)}")
        print(f"🟢 Active (Never Triggered): {colored(str(active), Colors.GREEN + Colors.BOLD)}")
        print(f"🔴 Triggered: {colored(str(triggered), Colors.RED + Colors.BOLD)}")
        
        print(f"\n{colored('Canaries by Type:', Colors.BOLD)}")
        for ctype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {ctype}: {count}")
        
        print(f"\nTotal Access Events: {colored(str(len(logs)), Colors.YELLOW + Colors.BOLD)}")
        
        if logs:
            recent = logs[0]
            print(f"Most Recent Access: {recent['accessed_at'][:19]}")
        
    finally:
        db.close()


def cmd_export(args):
    """Export all canary tokens to JSON"""
    db = CanaryDB()
    
    try:
        canaries = db.list_canaries()
        logs = db.get_access_logs(limit=10000)
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'canaries': canaries,
            'access_logs': logs
        }
        
        output_file = args.output or f"canarydrop_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(colored(f"\n✓ Exported {len(canaries)} canaries and {len(logs)} logs", Colors.GREEN))
        print(f"File: {output_file}")
        
    finally:
        db.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='CanaryDrop CLI - Create and manage canary tokens for security monitoring',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new canary token')
    create_parser.add_argument('--type', '-t', required=True,
                              choices=['dns', 'http', 'aws-key', 'sql', 'email', 'api-key', 'qr-code', 'document'],
                              help='Type of canary token')
    create_parser.add_argument('--name', '-n', required=True, help='Name for the canary')
    create_parser.add_argument('--memo', '-m', help='Additional notes')
    create_parser.add_argument('--alert', '-a', default='console', help='Alert method')
    create_parser.add_argument('--destination', '-d', help='Alert destination')
    create_parser.add_argument('--url', help='Custom URL (for QR codes)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all canary tokens')
    list_parser.add_argument('--type', '-t', help='Filter by type')
    list_parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show access history')
    history_parser.add_argument('--token', '-t', help='Filter by token ID')
    history_parser.add_argument('--limit', '-l', type=int, default=100, help='Limit results')
    history_parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a canary token')
    delete_parser.add_argument('token_id', help='Token ID to delete')
    delete_parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show token details')
    info_parser.add_argument('token_id', help='Token ID')
    
    # Trigger command
    trigger_parser = subparsers.add_parser('trigger', help='Manually trigger a token (testing)')
    trigger_parser.add_argument('token_id', help='Token ID')
    trigger_parser.add_argument('--ip', help='IP address')
    trigger_parser.add_argument('--user-agent', help='User agent')
    trigger_parser.add_argument('--metadata', help='Additional metadata (JSON)')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export all data to JSON')
    export_parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to appropriate command
    commands = {
        'create': cmd_create,
        'list': cmd_list,
        'history': cmd_history,
        'delete': cmd_delete,
        'info': cmd_info,
        'trigger': cmd_trigger,
        'stats': cmd_stats,
        'export': cmd_export
    }
    
    commands[args.command](args)


if __name__ == '__main__':
    main()
