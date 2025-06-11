# Documentation Guide for Beginners

Welcome to the complete guide for understanding and contributing to this project's documentation! This guide is designed for newcomers who want to learn how to use, maintain, and contribute to our MkDocs-based documentation system.

## 🎯 What You'll Learn

- How our documentation system works
- How to view and navigate the docs
- How to edit and contribute content
- Best practices for writing documentation

## 📚 Understanding Our Documentation System

### What is MkDocs?

**MkDocs** is a fast, simple static site generator designed for building project documentation. Think of it as a tool that takes plain text files (written in Markdown) and converts them into a beautiful, searchable website.

### Why We Chose MkDocs

We migrated from `pdoc3` to MkDocs because it offers:

- ✅ **Better for mixed content**: API docs + tutorials + guides
- ✅ **Markdown-based**: Easy to write and edit
- ✅ **Beautiful themes**: Professional, responsive design
- ✅ **Great for research projects**: Perfect for academic/scientific documentation
- ✅ **Jupyter integration**: Can include notebook examples
- ✅ **Easy collaboration**: Version controlled with Git

### Documentation Structure

```
docs_new/
├── index.md                    # Homepage
├── getting-started/           # New user guides
│   ├── installation.md       # Setup instructions
│   ├── quick-start.md        # Basic usage
│   └── documentation-guide.md # This file!
├── user-guide/               # Detailed usage docs
├── api-reference/            # Auto-generated code docs
├── technical-notes/          # Implementation details
└── development/              # Contributing guides
```

## 🖥️ Viewing the Documentation

### Method 1: Local Development Server (Recommended)

This gives you a live preview that updates as you edit:

```bash
# Navigate to the project root
cd /path/to/ds4cg-job-analytics

# Activate your virtual environment
source duckdb/bin/activate

# Start the development server
mkdocs serve
```

!!! success "Live Documentation Server"
    Open `http://127.0.0.1:8000` in your browser. The docs will auto-reload when you save changes!

### Method 2: Build Static Site

Generate HTML files you can open directly:

```bash
mkdocs build
```

This creates a `site/` folder with HTML files you can open in any browser.

### Method 3: Deploy to GitHub Pages

For sharing with others:

```bash
mkdocs gh-deploy
```

This publishes your docs to `https://yourusername.github.io/ds4cg-job-analytics`

## ✏️ Editing Documentation

### Basic Markdown Syntax

Our docs use **Markdown**, a simple markup language. Here are the essentials:

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
`Code snippet`

- Bullet point
- Another bullet
  - Nested bullet

1. Numbered list
2. Another item

[Link text](https://example.com)

![Image alt text](path/to/image.png)
```

### Advanced Features

We use Material for MkDocs with extensions for extra features:

#### Code Blocks with Syntax Highlighting

```python
def analyze_gpu_usage(data):
    """Analyze GPU utilization patterns."""
    return data.groupby('GPUType').mean()
```

#### Admonitions (Callout Boxes)

```markdown
!!! tip "Pro Tip"
    Use admonitions to highlight important information!

!!! warning "Important"
    This will stand out to readers.

!!! info "Did You Know?"
    You can use different types: tip, warning, info, success, failure
```

#### Tabbed Content

```markdown
=== "Python"
    ```python
    print("Hello, World!")
    ```

=== "R"
    ```r
    print("Hello, World!")
    ```

=== "SQL"
    ```sql
    SELECT 'Hello, World!' as greeting;
    ```
```

#### Math Equations

```markdown
The efficiency formula is: $\text{efficiency} = \frac{\text{used resources}}{\text{requested resources}}$
```

## 📝 Adding New Documentation

### Step 1: Create a New File

```bash
# Create a new documentation file
touch docs_new/user-guide/new-feature.md
```

### Step 2: Add Content

```markdown
# New Feature Guide

Brief description of what this feature does.

## Overview

Detailed explanation...

## Usage Examples

```bash
python script.py --new-feature
```

## Troubleshooting

Common issues and solutions...
```

### Step 3: Update Navigation

Edit `mkdocs.yml` to add your new page:

```yaml
nav:
  - Home: index.md
  - User Guide:
    - Dashboard: user-guide/dashboard.md
    - New Feature: user-guide/new-feature.md  # Add this line
```

### Step 4: Test Your Changes

```bash
mkdocs serve
```

Check that your new page appears in the navigation and displays correctly.

## 🔄 API Documentation

Our setup automatically generates API documentation from code docstrings!

### How It Works

The `mkdocstrings` plugin reads docstrings from your Python code and creates documentation pages. For example:

```python
def calculate_efficiency(used_memory: float, total_memory: float) -> float:
    """Calculate GPU memory utilization efficiency.
    
    Args:
        used_memory: Amount of memory used in GB
        total_memory: Total available memory in GB
        
    Returns:
        Efficiency ratio between 0 and 1
        
    Example:
        >>> calculate_efficiency(40, 80)
        0.5
    """
    return used_memory / total_memory
```

### Adding API Documentation

To document a new module, create a file like `docs_new/api-reference/new-module.md`:

```markdown
# New Module API

::: src.path.to.new_module
    options:
      show_source: true
      show_root_heading: true
```

The `::: src.path.to.new_module` syntax tells mkdocstrings to automatically generate documentation from that module.

## 🎨 Customizing Appearance

### Themes and Colors

Edit `mkdocs.yml` to change the look:

```yaml
theme:
  name: material
  palette:
    primary: blue  # Change to: red, green, purple, etc.
    accent: blue
```

### Adding Custom CSS

Create `docs_new/stylesheets/extra.css`:

```css
.md-header {
    background-color: #2c3e50 !important;
}
```

Then reference it in `mkdocs.yml`:

```yaml
extra_css:
  - stylesheets/extra.css
```

## 📋 Documentation Workflow

### For Small Changes

1. Edit the Markdown file directly
2. Preview with `mkdocs serve`
3. Commit and push changes

### For Major Changes

1. Create a new branch: `git checkout -b improve-docs`
2. Make your changes
3. Test thoroughly: `mkdocs serve`
4. Create a pull request

### Regular Maintenance

- **Update API docs**: They update automatically when code changes
- **Review for accuracy**: Check that examples still work
- **Update screenshots**: Keep visual content current
- **Check links**: Ensure external links still work

## 🧪 Testing Documentation

### Before Publishing

Always test your documentation:

```bash
# Check for broken links and issues
mkdocs build --strict

# Serve locally and review
mkdocs serve

# Test all code examples work
python -c "exec(open('docs_new/examples/test.py').read())"
```

### Common Issues

!!! warning "Broken Links"
    - Always use relative links: `[text](../other-page.md)`
    - Check that file paths are correct

!!! warning "Missing Images"
    - Store images in `docs_new/images/`
    - Use relative paths: `![alt](../images/screenshot.png)`

!!! warning "Code Examples"
    - Test all code snippets actually work
    - Use consistent indentation
    - Include necessary imports

## 🤝 Best Practices

### Writing Style

- **Be clear and concise**: Explain complex concepts simply
- **Use examples**: Show, don't just tell
- **Be consistent**: Use the same terms throughout
- **Think like a beginner**: What would you want to know?

### Organization

- **Logical structure**: Group related content together
- **Progressive disclosure**: Start simple, add complexity gradually
- **Cross-references**: Link to related sections
- **Table of contents**: Use headings to create structure

### Maintenance

- **Keep it current**: Update docs when code changes
- **Version control**: Use meaningful commit messages
- **Regular reviews**: Schedule documentation audits
- **User feedback**: Listen to what users find confusing

## 🆘 Getting Help

### Resources

- **MkDocs Documentation**: [mkdocs.org](https://www.mkdocs.org/)
- **Material Theme**: [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
- **Markdown Guide**: [markdownguide.org](https://www.markdownguide.org/)

### Common Commands

```bash
# Start development server
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy

# Clean build directory
mkdocs build --clean

# Get help
mkdocs --help
```

### Troubleshooting

!!! failure "Module Import Errors"
    Make sure your Python path includes the src directory:
    ```bash
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    ```

!!! failure "Theme Not Found"
    Install missing theme:
    ```bash
    pip install mkdocs-material
    ```

!!! failure "Plugin Errors"
    Check that all plugins are installed:
    ```bash
    pip install mkdocstrings[python] mkdocs-jupyter
    ```

## 🎓 Next Steps

Now that you understand our documentation system:

1. **Practice**: Edit this page to add your own tips!
2. **Contribute**: Find a section that could be improved
3. **Expand**: Add documentation for undocumented features
4. **Share**: Help other team members learn this workflow

## 📚 Advanced Topics

### Jupyter Notebook Integration

You can include Jupyter notebooks directly in the documentation:

```markdown
# Analysis Example

Here's an interactive analysis notebook:

{{ notebooks/example_analysis.ipynb }}
```

### Custom Macros

Create reusable content snippets in `mkdocs.yml`:

```yaml
extra:
  example_command: "python gpu_metrics.py waittime"
```

Then use: `{{ example_command }}` in any Markdown file.

### Internationalization

For multi-language documentation:

```yaml
plugins:
  - i18n:
      default_language: en
      languages:
        en: English
        es: Español
```

---

**Congratulations!** 🎉 You now have all the tools needed to contribute to and maintain our documentation. Remember, good documentation is a team effort - every improvement helps make the project more accessible to new users and contributors.
