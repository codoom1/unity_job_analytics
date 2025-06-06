"""
Script to generate documentation for all Python modules in the src/ directory using pdoc3.
Outputs documentation to docs/auto_docs/.
"""
import os
import subprocess

SRC_DIR = os.path.join(os.path.dirname(__file__), '..', 'src')
DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'auto_docs')

if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)

# Find all Python modules/packages in src, but skip __init__.py files
modules = []
for root, dirs, files in os.walk(SRC_DIR):
    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            rel_path = os.path.relpath(os.path.join(root, file), SRC_DIR)
            module = rel_path[:-3].replace(os.sep, '.')  # remove .py and convert to module path
            # Only include modules with their package prefix (e.g., analytics.gpu_metrics)
            # Skip top-level modules (like db_utils) unless src is in PYTHONPATH
            if '.' in module:
                modules.append(module)
            else:
                # For top-level modules, add src to PYTHONPATH for pdoc3 to find them
                pass

# Set PYTHONPATH to include src so pdoc3 can find top-level modules
env = os.environ.copy()
env['PYTHONPATH'] = SRC_DIR + os.pathsep + env.get('PYTHONPATH', '')

# Generate docs for all modules at once
cmd = [
    'pdoc3',
    '--output-dir', DOCS_DIR,
    '--force',
] + modules

print(f"Generating documentation for modules: {modules}")
subprocess.run(cmd, check=True, env=env)
print(f"Documentation generated in {DOCS_DIR}")
