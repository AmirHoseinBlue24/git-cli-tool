#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional Git CLI Tool
A user-friendly wrapper for Git operations
Created by Claude AI Assistant
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import re
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GitError(Exception):
    """Custom exception for Git operations"""
    pass

class GitTool:
    """Professional Git CLI Tool with enhanced features"""
    
    def __init__(self):
        self.current_repo = None
        self.config_file = Path.home() / '.gitool_config.json'
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'default_branch': 'main',
            'auto_push': False,
            'preferred_repos': [],
            'commit_template': ''
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.print_error(f"Error saving config: {e}")
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"{Colors.OKBLUE}ℹ {message}{Colors.ENDC}")
    
    def print_header(self, message: str):
        """Print header message"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}")
    
    def run_command(self, command: List[str], capture_output: bool = False) -> Optional[str]:
        """Run a system command safely"""
        try:
            if capture_output:
                result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
                if result.returncode != 0:
                    raise GitError(f"Command failed: {' '.join(command)}\n{result.stderr}")
                return result.stdout.strip()
            else:
                result = subprocess.run(command, encoding='utf-8')
                if result.returncode != 0:
                    raise GitError(f"Command failed: {' '.join(command)}")
                return None
        except FileNotFoundError:
            raise GitError(f"Command not found: {command[0]}")
        except Exception as e:
            raise GitError(f"Error running command: {e}")
    
    def is_git_repo(self, path: str = '.') -> bool:
        """Check if current directory is a git repository"""
        try:
            self.run_command(['git', 'rev-parse', '--git-dir'], capture_output=True)
            return True
        except:
            return False
    
    def get_current_branch(self) -> str:
        """Get current branch name"""
        try:
            return self.run_command(['git', 'branch', '--show-current'], capture_output=True)
        except:
            return 'main'
    
    def get_remote_branches(self) -> List[str]:
        """Get list of remote branches"""
        try:
            output = self.run_command(['git', 'branch', '-r'], capture_output=True)
            branches = []
            for line in output.split('\n'):
                line = line.strip()
                if line and not line.startswith('origin/HEAD'):
                    branch = line.replace('origin/', '')
                    branches.append(branch)
            return branches
        except:
            return []
    
    def get_local_branches(self) -> List[str]:
        """Get list of local branches"""
        try:
            output = self.run_command(['git', 'branch'], capture_output=True)
            branches = []
            for line in output.split('\n'):
                line = line.strip()
                if line:
                    branch = line.replace('* ', '')
                    branches.append(branch)
            return branches
        except:
            return []
    
    def get_status(self) -> Dict[str, List[str]]:
        """Get repository status"""
        try:
            output = self.run_command(['git', 'status', '--porcelain'], capture_output=True)
            status = {
                'modified': [],
                'added': [],
                'deleted': [],
                'renamed': [],
                'untracked': []
            }
            
            for line in output.split('\n'):
                if len(line) >= 3:
                    status_code = line[:2]
                    filename = line[3:]
                    
                    if status_code == '??':
                        status['untracked'].append(filename)
                    elif 'M' in status_code:
                        status['modified'].append(filename)
                    elif 'A' in status_code:
                        status['added'].append(filename)
                    elif 'D' in status_code:
                        status['deleted'].append(filename)
                    elif 'R' in status_code:
                        status['renamed'].append(filename)
            
            return status
        except:
            return {'modified': [], 'added': [], 'deleted': [], 'renamed': [], 'untracked': []}
    
    def select_repository(self) -> str:
        """Interactive repository selection"""
        self.print_header("📁 Repository Selection")
        
        current_dir = os.getcwd()
        if self.is_git_repo():
            print(f"Current directory is a Git repository: {Colors.OKGREEN}{current_dir}{Colors.ENDC}")
            use_current = input("Use current directory? (Y/n): ").lower()
            if use_current != 'n':
                return current_dir
        
        print("\nOptions:")
        print("1. Enter repository path")
        print("2. Browse recent repositories")
        print("3. Initialize new repository")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            repo_path = input("Enter repository path: ").strip()
            if os.path.isdir(repo_path):
                os.chdir(repo_path)
                if not self.is_git_repo():
                    self.print_error("Not a Git repository")
                    return self.select_repository()
                return repo_path
            else:
                self.print_error("Directory not found")
                return self.select_repository()
        
        elif choice == '2':
            if self.config['preferred_repos']:
                print("\nRecent repositories:")
                for i, repo in enumerate(self.config['preferred_repos'], 1):
                    print(f"{i}. {repo}")
                
                try:
                    repo_choice = int(input("\nSelect repository: ")) - 1
                    if 0 <= repo_choice < len(self.config['preferred_repos']):
                        repo_path = self.config['preferred_repos'][repo_choice]
                        os.chdir(repo_path)
                        return repo_path
                except:
                    pass
            
            self.print_warning("No recent repositories found")
            return self.select_repository()
        
        elif choice == '3':
            return self.init_repository()
        
        else:
            self.print_error("Invalid choice")
            return self.select_repository()
    
    def init_repository(self) -> str:
        """Initialize new Git repository"""
        self.print_header("🆕 Initialize New Repository")
        
        repo_name = input("Repository name: ").strip()
        if not repo_name:
            self.print_error("Repository name required")
            return self.init_repository()
        
        repo_path = Path.cwd() / repo_name
        
        try:
            repo_path.mkdir(exist_ok=True)
            os.chdir(repo_path)
            
            self.run_command(['git', 'init'])
            self.run_command(['git', 'branch', '-M', self.config['default_branch']])
            
            # Create initial files
            readme_content = f"# {repo_name}\n\nDescription of your project.\n"
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env
.venv
env/
venv/
"""
            with open('.gitignore', 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            
            self.run_command(['git', 'add', '.'])
            self.run_command(['git', 'commit', '-m', 'Initial commit'])
            
            self.print_success(f"Repository initialized: {repo_path}")
            
            # Add to preferred repos
            if str(repo_path) not in self.config['preferred_repos']:
                self.config['preferred_repos'].insert(0, str(repo_path))
                self.config['preferred_repos'] = self.config['preferred_repos'][:10]  # Keep last 10
                self.save_config()
            
            return str(repo_path)
        
        except Exception as e:
            self.print_error(f"Error initializing repository: {e}")
            return self.select_repository()
    
    def select_branch(self) -> str:
        """Interactive branch selection"""
        self.print_header("🌿 Branch Selection")
        
        current_branch = self.get_current_branch()
        local_branches = self.get_local_branches()
        remote_branches = self.get_remote_branches()
        
        print(f"Current branch: {Colors.OKGREEN}{current_branch}{Colors.ENDC}")
        
        if local_branches:
            print(f"\nLocal branches:")
            for branch in local_branches:
                marker = "* " if branch == current_branch else "  "
                print(f"{marker}{branch}")
        
        if remote_branches:
            print(f"\nRemote branches:")
            for branch in remote_branches:
                if branch not in local_branches:
                    print(f"  {branch} (remote)")
        
        print(f"\nOptions:")
        print(f"1. Stay on current branch ({current_branch})")
        print(f"2. Switch to existing branch")
        print(f"3. Create new branch")
        print(f"4. Create and switch to new branch")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            return current_branch
        
        elif choice == '2':
            available_branches = local_branches + [b for b in remote_branches if b not in local_branches]
            if not available_branches:
                self.print_warning("No other branches available")
                return current_branch
            
            print("\nAvailable branches:")
            for i, branch in enumerate(available_branches, 1):
                remote_marker = " (remote)" if branch in remote_branches and branch not in local_branches else ""
                print(f"{i}. {branch}{remote_marker}")
            
            try:
                branch_choice = int(input("\nSelect branch: ")) - 1
                if 0 <= branch_choice < len(available_branches):
                    target_branch = available_branches[branch_choice]
                    
                    if target_branch in remote_branches and target_branch not in local_branches:
                        self.run_command(['git', 'checkout', '-b', target_branch, f'origin/{target_branch}'])
                    else:
                        self.run_command(['git', 'checkout', target_branch])
                    
                    self.print_success(f"Switched to branch: {target_branch}")
                    return target_branch
            except:
                pass
            
            self.print_error("Invalid choice")
            return self.select_branch()
        
        elif choice == '3':
            branch_name = input("New branch name: ").strip()
            if branch_name:
                try:
                    self.run_command(['git', 'branch', branch_name])
                    self.print_success(f"Created branch: {branch_name}")
                    return current_branch
                except Exception as e:
                    self.print_error(f"Error creating branch: {e}")
            return self.select_branch()
        
        elif choice == '4':
            branch_name = input("New branch name: ").strip()
            if branch_name:
                try:
                    self.run_command(['git', 'checkout', '-b', branch_name])
                    self.print_success(f"Created and switched to branch: {branch_name}")
                    return branch_name
                except Exception as e:
                    self.print_error(f"Error creating branch: {e}")
            return self.select_branch()
        
        else:
            self.print_error("Invalid choice")
            return self.select_branch()
    
    def add_files(self):
        """Interactive file addition"""
        self.print_header("📝 Add Files to Repository")
        
        status = self.get_status()
        all_files = status['modified'] + status['untracked'] + status['deleted']
        
        if not all_files:
            self.print_info("No files to add")
            return
        
        print("Files to add:")
        print("0. Add all files")
        
        for i, file in enumerate(all_files, 1):
            file_status = "modified" if file in status['modified'] else \
                         "deleted" if file in status['deleted'] else "untracked"
            print(f"{i}. {file} ({file_status})")
        
        choices = input("\nSelect files (comma-separated numbers, 0 for all): ").strip()
        
        if not choices:
            return
        
        try:
            if '0' in choices:
                self.run_command(['git', 'add', '.'])
                self.print_success("All files added")
            else:
                selected_indices = [int(x.strip()) - 1 for x in choices.split(',')]
                selected_files = [all_files[i] for i in selected_indices if 0 <= i < len(all_files)]
                
                if selected_files:
                    self.run_command(['git', 'add'] + selected_files)
                    self.print_success(f"Added {len(selected_files)} files")
                else:
                    self.print_error("No valid files selected")
        
        except Exception as e:
            self.print_error(f"Error adding files: {e}")
    
    def commit_changes(self):
        """Interactive commit creation"""
        self.print_header("💾 Commit Changes")
        
        # Check if there are staged changes
        try:
            output = self.run_command(['git', 'diff', '--cached', '--name-only'], capture_output=True)
            if not output:
                self.print_warning("No staged changes to commit")
                return
        except:
            self.print_warning("Error checking staged changes")
            return
        
        # Show staged files
        print("Staged files:")
        for file in output.split('\n'):
            if file.strip():
                print(f"  {Colors.OKGREEN}+ {file}{Colors.ENDC}")
        
        # Commit message
        commit_msg = input("\nCommit message: ").strip()
        if not commit_msg:
            self.print_error("Commit message required")
            return
        
        # Detailed description (optional)
        detailed = input("Detailed description (optional, press Enter to skip): ").strip()
        
        full_message = commit_msg
        if detailed:
            full_message += f"\n\n{detailed}"
        
        try:
            self.run_command(['git', 'commit', '-m', full_message])
            self.print_success("Changes committed successfully")
            
            # Auto-push if configured
            if self.config.get('auto_push', False):
                push_choice = input("Auto-push enabled. Push now? (Y/n): ").lower()
                if push_choice != 'n':
                    self.push_changes()
        
        except Exception as e:
            self.print_error(f"Error committing changes: {e}")
    
    def push_changes(self):
        """Push changes to remote repository"""
        self.print_header("🚀 Push Changes")
        
        current_branch = self.get_current_branch()
        
        try:
            # Check if remote exists
            remotes = self.run_command(['git', 'remote'], capture_output=True)
            if not remotes:
                self.print_warning("No remote repository configured")
                
                remote_url = input("Enter remote repository URL (or press Enter to skip): ").strip()
                if remote_url:
                    self.run_command(['git', 'remote', 'add', 'origin', remote_url])
                    self.print_success("Remote repository added")
                else:
                    return
            
            # Push changes
            self.run_command(['git', 'push', 'origin', current_branch])
            self.print_success(f"Changes pushed to {current_branch}")
        
        except Exception as e:
            self.print_error(f"Error pushing changes: {e}")
    
    def pull_changes(self):
        """Pull changes from remote repository"""
        self.print_header("⬇️ Pull Changes")
        
        current_branch = self.get_current_branch()
        
        try:
            self.run_command(['git', 'pull', 'origin', current_branch])
            self.print_success(f"Changes pulled from {current_branch}")
        except Exception as e:
            self.print_error(f"Error pulling changes: {e}")
    
    def show_status(self):
        """Show repository status"""
        self.print_header("📊 Repository Status")
        
        try:
            current_branch = self.get_current_branch()
            print(f"Current branch: {Colors.OKGREEN}{current_branch}{Colors.ENDC}")
            
            status = self.get_status()
            
            if status['modified']:
                print(f"\n{Colors.WARNING}Modified files:{Colors.ENDC}")
                for file in status['modified']:
                    print(f"  M {file}")
            
            if status['added']:
                print(f"\n{Colors.OKGREEN}Added files:{Colors.ENDC}")
                for file in status['added']:
                    print(f"  A {file}")
            
            if status['deleted']:
                print(f"\n{Colors.FAIL}Deleted files:{Colors.ENDC}")
                for file in status['deleted']:
                    print(f"  D {file}")
            
            if status['untracked']:
                print(f"\n{Colors.OKCYAN}Untracked files:{Colors.ENDC}")
                for file in status['untracked']:
                    print(f"  ? {file}")
            
            if not any(status.values()):
                print(f"\n{Colors.OKGREEN}Working tree clean{Colors.ENDC}")
            
            # Show recent commits
            try:
                commits = self.run_command(['git', 'log', '--oneline', '-5'], capture_output=True)
                if commits:
                    print(f"\n{Colors.OKBLUE}Recent commits:{Colors.ENDC}")
                    for commit in commits.split('\n'):
                        print(f"  {commit}")
            except:
                pass
        
        except Exception as e:
            self.print_error(f"Error getting status: {e}")
    
    def show_log(self):
        """Show commit history"""
        self.print_header("📜 Commit History")
        
        try:
            self.run_command(['git', 'log', '--oneline', '--graph', '--decorate', '-10'])
        except Exception as e:
            self.print_error(f"Error showing log: {e}")
    
    def manage_branches(self):
        """Branch management menu"""
        self.print_header("🌿 Branch Management")
        
        while True:
            current_branch = self.get_current_branch()
            print(f"\nCurrent branch: {Colors.OKGREEN}{current_branch}{Colors.ENDC}")
            
            print("\nBranch operations:")
            print("1. List branches")
            print("2. Create branch")
            print("3. Switch branch")
            print("4. Delete branch")
            print("5. Merge branch")
            print("6. Back to main menu")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                self.show_branches()
            elif choice == '2':
                self.create_branch()
            elif choice == '3':
                self.select_branch()
            elif choice == '4':
                self.delete_branch()
            elif choice == '5':
                self.merge_branch()
            elif choice == '6':
                break
            else:
                self.print_error("Invalid choice")
    
    def show_branches(self):
        """Show all branches"""
        local_branches = self.get_local_branches()
        remote_branches = self.get_remote_branches()
        current_branch = self.get_current_branch()
        
        if local_branches:
            print(f"\n{Colors.OKBLUE}Local branches:{Colors.ENDC}")
            for branch in local_branches:
                marker = f"{Colors.OKGREEN}* {Colors.ENDC}" if branch == current_branch else "  "
                print(f"{marker}{branch}")
        
        if remote_branches:
            print(f"\n{Colors.OKCYAN}Remote branches:{Colors.ENDC}")
            for branch in remote_branches:
                print(f"  origin/{branch}")
    
    def create_branch(self):
        """Create new branch"""
        branch_name = input("New branch name: ").strip()
        if not branch_name:
            return
        
        try:
            self.run_command(['git', 'branch', branch_name])
            self.print_success(f"Created branch: {branch_name}")
            
            switch = input("Switch to new branch? (Y/n): ").lower()
            if switch != 'n':
                self.run_command(['git', 'checkout', branch_name])
                self.print_success(f"Switched to branch: {branch_name}")
        
        except Exception as e:
            self.print_error(f"Error creating branch: {e}")
    
    def delete_branch(self):
        """Delete branch"""
        branches = self.get_local_branches()
        current_branch = self.get_current_branch()
        
        deletable_branches = [b for b in branches if b != current_branch]
        
        if not deletable_branches:
            self.print_warning("No branches to delete")
            return
        
        print("\nBranches to delete:")
        for i, branch in enumerate(deletable_branches, 1):
            print(f"{i}. {branch}")
        
        try:
            choice = int(input("\nSelect branch to delete: ")) - 1
            if 0 <= choice < len(deletable_branches):
                branch_to_delete = deletable_branches[choice]
                
                confirm = input(f"Delete branch '{branch_to_delete}'? (y/N): ").lower()
                if confirm == 'y':
                    self.run_command(['git', 'branch', '-d', branch_to_delete])
                    self.print_success(f"Deleted branch: {branch_to_delete}")
        
        except Exception as e:
            self.print_error(f"Error deleting branch: {e}")
    
    def merge_branch(self):
        """Merge branch"""
        branches = self.get_local_branches()
        current_branch = self.get_current_branch()
        
        mergeable_branches = [b for b in branches if b != current_branch]
        
        if not mergeable_branches:
            self.print_warning("No branches to merge")
            return
        
        print(f"\nMerging into: {Colors.OKGREEN}{current_branch}{Colors.ENDC}")
        print("\nAvailable branches:")
        for i, branch in enumerate(mergeable_branches, 1):
            print(f"{i}. {branch}")
        
        try:
            choice = int(input("\nSelect branch to merge: ")) - 1
            if 0 <= choice < len(mergeable_branches):
                branch_to_merge = mergeable_branches[choice]
                
                self.run_command(['git', 'merge', branch_to_merge])
                self.print_success(f"Merged {branch_to_merge} into {current_branch}")
        
        except Exception as e:
            self.print_error(f"Error merging branch: {e}")
    
    def settings(self):
        """Configuration settings"""
        self.print_header("⚙️ Settings")
        
        while True:
            print(f"\nCurrent settings:")
            print(f"1. Default branch: {Colors.OKGREEN}{self.config['default_branch']}{Colors.ENDC}")
            print(f"2. Auto-push: {Colors.OKGREEN if self.config['auto_push'] else Colors.FAIL}{self.config['auto_push']}{Colors.ENDC}")
            print(f"3. Preferred repositories: {len(self.config['preferred_repos'])} saved")
            print(f"4. Clear preferred repositories")
            print(f"5. Back to main menu")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                new_branch = input(f"Default branch (current: {self.config['default_branch']}): ").strip()
                if new_branch:
                    self.config['default_branch'] = new_branch
                    self.save_config()
                    self.print_success("Default branch updated")
            
            elif choice == '2':
                self.config['auto_push'] = not self.config['auto_push']
                self.save_config()
                self.print_success(f"Auto-push {'enabled' if self.config['auto_push'] else 'disabled'}")
            
            elif choice == '3':
                if self.config['preferred_repos']:
                    print("\nPreferred repositories:")
                    for i, repo in enumerate(self.config['preferred_repos'], 1):
                        print(f"{i}. {repo}")
                else:
                    print("\nNo preferred repositories saved")
            
            elif choice == '4':
                confirm = input("Clear all preferred repositories? (y/N): ").lower()
                if confirm == 'y':
                    self.config['preferred_repos'] = []
                    self.save_config()
                    self.print_success("Preferred repositories cleared")
            
            elif choice == '5':
                break
            
            else:
                self.print_error("Invalid choice")
    
    def quick_commit(self):
        """Quick add, commit, and push workflow"""
        self.print_header("⚡ Quick Commit")
        
        # Add all files
        try:
            self.run_command(['git', 'add', '.'])
            self.print_success("All files added")
        except Exception as e:
            self.print_error(f"Error adding files: {e}")
            return
        
        # Commit
        commit_msg = input("Commit message: ").strip()
        if not commit_msg:
            self.print_error("Commit message required")
            return
        
        try:
            self.run_command(['git', 'commit', '-m', commit_msg])
            self.print_success("Changes committed")
        except Exception as e:
            self.print_error(f"Error committing: {e}")
            return
        
        # Push
        push_choice = input("Push changes? (Y/n): ").lower()
        if push_choice != 'n':
            self.push_changes()
    
    def main_menu(self):
        """Main application menu"""
        self.print_header("🚀 Professional Git CLI Tool")
        print(f"{Colors.OKCYAN}Welcome to the enhanced Git experience!{Colors.ENDC}")
        
        # Repository selection
        self.current_repo = self.select_repository()
        
        # Add to preferred repos
        if self.current_repo not in self.config['preferred_repos']:
            self.config['preferred_repos'].insert(0, self.current_repo)
            self.config['preferred_repos'] = self.config['preferred_repos'][:10]
            self.save_config()
        
        while True:
            self.print_header("📋 Main Menu")
            print(f"Repository: {Colors.OKGREEN}{self.current_repo}{Colors.ENDC}")
            print(f"Branch: {Colors.OKGREEN}{self.get_current_branch()}{Colors.ENDC}")
            
            print("\nQuick actions:")
            print("1. 📊 Show status")
            print("2. 📝 Add files")
            print("3. 💾 Commit changes")
            print("4. 🚀 Push changes")
            print("5. ⬇️ Pull changes")
            print("6. ⚡ Quick commit (add + commit + push)")
            
            print("\nAdvanced:")
            print("7. 🌿 Branch management")
            print("8. 📜 Show commit history")
            print("9. 🔄 Switch repository")
            print("10. ⚙️ Settings")
            print("11. 🚪 Exit")
            
            choice = input(f"\n{Colors.BOLD}Select option (1-11): {Colors.ENDC}").strip()
            
            try:
                if choice == '1':
                    self.show_status()
                elif choice == '2':
                    self.add_files()
                elif choice == '3':
                    self.commit_changes()
                elif choice == '4':
                    self.push_changes()
                elif choice == '5':
                    self.pull_changes()
                elif choice == '6':
                    self.quick_commit()
                elif choice == '7':
                    self.manage_branches()
                elif choice == '8':
                    self.show_log()
                elif choice == '9':
                    self.current_repo = self.select_repository()
                elif choice == '10':
                    self.settings()
                elif choice == '11':
                    self.print_success("Thanks for using Git CLI Tool!")
                    break
                else:
                    self.print_error("Invalid choice")
            
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}Operation cancelled{Colors.ENDC}")
            except Exception as e:
                self.print_error(f"Unexpected error: {e}")
            
            input(f"\n{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")


def main():
    """Main application entry point"""
    try:
        # Check if Git is installed
        subprocess.run(['git', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.FAIL}✗ Git is not installed or not in PATH{Colors.ENDC}")
        print("Please install Git and try again.")
        sys.exit(1)
    
    # Create and run the Git tool
    git_tool = GitTool()
    
    try:
        git_tool.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Application interrupted by user{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Fatal error: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()