#!/usr/bin/env python3
"""
Script to build and serve MkDocs documentation for the SLURM Job Analytics project.
This replaces the old pdoc3-based documentation generation.
"""
import os
import subprocess
import sys
import argparse
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_SOURCE = PROJECT_ROOT / "docs_new"
DOCS_OUTPUT = PROJECT_ROOT / "site"
MKDOCS_CONFIG = PROJECT_ROOT / "mkdocs.yml"

def check_mkdocs_installed():
    """Check if MkDocs and required plugins are installed."""
    try:
        result = subprocess.run(['mkdocs', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✓ MkDocs found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ MkDocs not found. Please install it with:")
        print("  pip install mkdocs mkdocs-material mkdocstrings[python] mkdocs-jupyter")
        return False

def build_docs(clean=True):
    """Build the MkDocs documentation."""
    if not check_mkdocs_installed():
        return False
    
    cmd = ['mkdocs', 'build']
    if clean:
        cmd.append('--clean')
    
    print(f"Building documentation from {DOCS_SOURCE} to {DOCS_OUTPUT}...")
    try:
        subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
        print(f"✓ Documentation built successfully in {DOCS_OUTPUT}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to build documentation: {e}")
        return False

def serve_docs(port=8000, host='127.0.0.1'):
    """Serve the MkDocs documentation with live reload."""
    if not check_mkdocs_installed():
        return False
    
    cmd = ['mkdocs', 'serve', '--dev-addr', f'{host}:{port}']
    
    print(f"Starting development server at http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to start server: {e}")
        return False
    return True

def deploy_docs():
    """Deploy documentation to GitHub Pages."""
    if not check_mkdocs_installed():
        return False
    
    print("Deploying documentation to GitHub Pages...")
    try:
        subprocess.run(['mkdocs', 'gh-deploy'], cwd=PROJECT_ROOT, check=True)
        print("✓ Documentation deployed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to deploy documentation: {e}")
        return False

def validate_setup():
    """Validate that the documentation setup is correct."""
    print("Validating MkDocs setup...")
    
    # Check if config file exists
    if not MKDOCS_CONFIG.exists():
        print(f"✗ MkDocs config file not found: {MKDOCS_CONFIG}")
        return False
    print(f"✓ Config file found: {MKDOCS_CONFIG}")
    
    # Check if docs source directory exists
    if not DOCS_SOURCE.exists():
        print(f"✗ Documentation source directory not found: {DOCS_SOURCE}")
        return False
    print(f"✓ Documentation source found: {DOCS_SOURCE}")
    
    # Check if key files exist
    key_files = [
        DOCS_SOURCE / "index.md",
        DOCS_SOURCE / "getting-started" / "installation.md",
        DOCS_SOURCE / "getting-started" / "documentation-guide.md",
    ]
    
    for file_path in key_files:
        if file_path.exists():
            print(f"✓ Found: {file_path.relative_to(PROJECT_ROOT)}")
        else:
            print(f"✗ Missing: {file_path.relative_to(PROJECT_ROOT)}")
    
    # Test build
    print("\nTesting documentation build...")
    return build_docs(clean=False)

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Build and serve MkDocs documentation for SLURM Job Analytics"
    )
    parser.add_argument('command', 
                       choices=['build', 'serve', 'deploy', 'validate'],
                       help='Command to execute')
    parser.add_argument('--clean', action='store_true',
                       help='Clean the output directory before building')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port for the development server (default: 8000)')
    parser.add_argument('--host', default='127.0.0.1',
                       help='Host for the development server (default: 127.0.0.1)')
    
    args = parser.parse_args()
    
    if args.command == 'build':
        success = build_docs(clean=args.clean)
    elif args.command == 'serve':
        success = serve_docs(port=args.port, host=args.host)
    elif args.command == 'deploy':
        success = deploy_docs()
    elif args.command == 'validate':
        success = validate_setup()
    else:
        parser.print_help()
        return 1
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
