# 🚀 Git CLI Tool

A professional, user-friendly Git command-line wrapper that makes Git operations intuitive and efficient.

## ✨ Features

### 🎯 Core Functionality
- **Interactive Repository Management**: Easy repository selection and switching
- **Smart Branch Operations**: Create, switch, merge, and delete branches with ease
- **Streamlined File Management**: Add files with visual selection
- **Intelligent Commit System**: Guided commit creation with optional detailed descriptions
- **Automated Push/Pull**: Seamless remote repository synchronization

### 🛠️ Advanced Features
- **Quick Commit Workflow**: One-command add, commit, and push
- **Repository Status Dashboard**: Visual representation of repository state
- **Branch Management Suite**: Complete branch lifecycle management
- **Configuration System**: Persistent settings and preferences
- **Repository History**: Recent repositories quick access
- **Auto-initialization**: Create new repositories with best practices

### 🎨 User Experience
- **Colorful Interface**: Beautiful terminal output with color coding
- **Error Handling**: Comprehensive error messages and recovery
- **Persian/English Support**: Full Unicode support for commit messages
- **Keyboard Shortcuts**: Efficient navigation and operation
- **Progress Indicators**: Visual feedback for long-running operations

## 📋 Requirements

- Python 3.7+
- Git (installed and in PATH)
- Terminal with color support (recommended)

## 🔧 Installation

### Option 1: pip
```bash
# Download package
pip install git-cli-tool==1.0.0

#Run from anywhere
gitool
```

### Option 2: Direct Download
```bash
# Download the script
curl -O https://raw.githubusercontent.com/AmirHoseinBlue24/git-cli-tool/main/git_cli_tool.py

# Make it executable
chmod +x git_cli_tool.py

# Run directly
python git_cli_tool.py
```

### Option 3: Package Installation
```bash
# Clone the repository
git clone https://github.com/AmirHoseinBlue24/git-cli-tool.git
cd git-cli-tool

# Install as package
pip install -e .

# Run from anywhere
gitool
```

### Option 4: System-wide Installation
```bash
# Copy to system path
sudo cp git_cli_tool.py /usr/local/bin/gitool
sudo chmod +x /usr/local/bin/gitool

# Run from anywhere
gitool
```

## 🚀 Quick Start

1. **Launch the tool**:
   ```bash
   python git_cli_tool.py
   ```

2. **Select or create a repository**:
   - Use existing repository
   - Browse recent repositories
   - Initialize new repository

3. **Choose your workflow**:
   - **Quick commit**: Add all files, commit, and push in one go
   - **Manual control**: Step-by-step file management
   - **Branch management**: Create and switch branches easily

## 📖 Usage Guide

### 🏠 Main Menu Options

| Option | Description | Usage |
|--------|-------------|-------|
| 📊 Show Status | Display repository status with visual indicators | View modified, added, deleted, and untracked files |
| 📝 Add Files | Interactive file selection for staging | Choose specific files or add all changes |
| 💾 Commit Changes | Create commits with guided prompts | Add commit message and optional description |
| 🚀 Push Changes | Push commits to remote repository | Automatic remote detection and branch pushing |
| ⬇️ Pull Changes | Pull latest changes from remote | Sync with remote repository |
| ⚡ Quick Commit | One-step add, commit, and push | Fastest way to save and sync changes |

### 🌿 Branch Management

```bash
# The tool provides interactive branch management:
- List all local and remote branches
- Create new branches with automatic switching
- Delete branches with safety confirmations
- Merge branches with conflict detection
- Switch between branches seamlessly
```

### ⚙️ Configuration

The tool maintains configuration in `~/.gitool_config.json`:

```json
{
  "default_branch": "main",
  "auto_push": false,
  "preferred_repos": [
    "/path/to/your/repo1",
    "/path/to/your/repo2"
  ],
  "commit_template": ""
}
```

## 🎯 Common Workflows

### 📝 Basic Development Workflow
1. Launch tool and select repository
2. Check status to see changes
3. Add files (specific or all)
4. Commit with descriptive message
5. Push to remote repository

### 🔄 Feature Development
1. Create new feature branch
2. Make changes and commit regularly
3. Push feature branch
4. Merge back to main branch
5. Delete feature branch

### ⚡ Quick Updates
1. Use "Quick Commit" option
2. Enter commit message
3. Everything is handled automatically

## 🎨 Visual Features

### Color Coding
- 🟢 **Green**: Success messages, current branch, clean files
- 🔴 **Red**: Error messages, deleted files
- 🟡 **Yellow**: Warning messages, modified files
- 🔵 **Blue**: Information messages, branch names
- 🟣 **Purple**: Headers and titles
- 🔷 **Cyan**: Untracked files, special info

### Status Indicators
- `✓` Success operations
- `✗` Error conditions
- `⚠` Warning messages
- `ℹ` Information
- `*` Current branch
- `+` Added files
- `M` Modified files
- `D` Deleted files
- `?` Untracked files

## 🔧 Advanced Configuration

### Environment Variables
```bash
# Set default configuration
export GITOOL_DEFAULT_BRANCH="main"
export GITOOL_AUTO_PUSH="true"
export GITOOL_EDITOR="nano"
```

### Custom Commit Templates
Create commit templates for consistent messaging:
```bash
# In your repository
echo "feat: " > .gitmessage
git config commit.template .gitmessage
```

## 🐛 Troubleshooting

### Common Issues

**Git not found**:
```bash
# Install Git
sudo apt install git  # Ubuntu/Debian
brew install git       # macOS
```

**Permission denied**:
```bash
# Make script executable
chmod +x git_cli_tool.py
```

**Python version issues**:
```bash
# Check Python version
python --version
# Use Python 3 explicitly
python3 git_cli_tool.py
```

**Remote repository issues**:
```bash
# Check remote configuration
git remote -v
# Add remote if missing
git remote add origin https://github.com/AmirHoseinBlue24/git-cli-tool.git
```

### Error Recovery
- The tool provides helpful error messages
- Most operations can be retried
- Configuration is automatically backed up
- Safe defaults prevent data loss

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
# Clone for development
git clone https://github.com/AmirHoseinBlue24/git-cli-tool.git
cd git-cli-tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python standard library only
- Inspired by the need for better Git UX
- Designed for developers who value efficiency
- Created with ❤️ by AmirHoseinBlue24

## 🔗 Links

- [GitHub Repository](https://github.com/AmirHoseinBlue24/git-cli-tool)
- [Issue Tracker](https://github.com/AmirHoseinBlue24/git-cli-tool/issues)
- [Documentation](https://github.com/AmirHoseinBlue24/git-cli-tool/wiki)

---

**Made with ❤️ for the developer community**

*Transform your Git experience from complex to simple, from tedious to efficient.*