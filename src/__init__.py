"""
Git CLI Tool - Professional Git Wrapper
A user-friendly command-line tool for Git operations

Created with ❤️ for the developer community
"""

__version__ = "1.0.0"
__author__ = "AmirHoseinBlue"
__email__ = "amirakhlagh893@gmail.com"
__description__ = "A professional Git CLI wrapper with enhanced user experience"

from .git_cli_tool import GitTool, main

__all__ = ["GitTool", "main"]