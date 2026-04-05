#!/usr/bin/env python3
"""
DataFlow Pro - Pre-Submission Validation Script

This script checks that all project requirements are met before submission.
Run this before submitting to ensure you haven't missed anything!

Usage: python validate_submission.py
"""

import os
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_success(f"Found: {filepath}")
        return True
    else:
        if required:
            print_error(f"Missing: {filepath}")
        else:
            print_warning(f"Optional file missing: {filepath}")
        return False


def check_directory_exists(dirpath, required=True):
    """Check if a directory exists"""
    if Path(dirpath).is_dir():
        print_success(f"Found directory: {dirpath}")
        return True
    else:
        if required:
            print_error(f"Missing directory: {dirpath}")
        else:
            print_warning(f"Optional directory missing: {dirpath}")
        return False


def validate_file_structure():
    """Validate that all required files and directories exist"""
    print_header("FILE STRUCTURE VALIDATION")
    
    checks = []
    
    # Required directories
    print(f"\n{Colors.BOLD}Checking Required Directories:{Colors.END}")
    checks.append(check_directory_exists("data", required=True))
    checks.append(check_directory_exists("src", required=True))
    
    # Optional but recommended directories
    print(f"\n{Colors.BOLD}Checking Recommended Directories:{Colors.END}")
    check_directory_exists("tests", required=False)
    
    # Required data files
    print(f"\n{Colors.BOLD}Checking Data Files:{Colors.END}")
    checks.append(check_file_exists("data/sales_data.csv", required=True))
    
    # Required source files
    print(f"\n{Colors.BOLD}Checking Source Code Files:{Colors.END}")
    checks.append(check_file_exists("src/phase1_indexer.py", required=True))
    checks.append(check_file_exists("src/phase2_tracker.py", required=True))
    checks.append(check_file_exists("src/phase3_parser.py", required=True))
    checks.append(check_file_exists("src/phase4_buffer.py", required=True))
    checks.append(check_file_exists("src/phase5_trees.py", required=True))
    checks.append(check_file_exists("src/main.py", required=True))
    
    # Required documentation
    print(f"\n{Colors.BOLD}Checking Documentation Files:{Colors.END}")
    checks.append(check_file_exists("README.md", required=True))
    checks.append(check_file_exists("requirements.txt", required=True))
    
    # Required deliverables
    print(f"\n{Colors.BOLD}Checking Required Deliverables:{Colors.END}")
    checks.append(check_file_exists("logs.txt", required=True))
    
    # Check for performance report (could be in docs/ or root)
    perf_report_found = False
    if Path("PERFORMANCE_REPORT.md").exists():
        print_success("Found: PERFORMANCE_REPORT.md (in root)")
        perf_report_found = True
    elif Path("docs/PERFORMANCE_REPORT.md").exists():
        print_success("Found: docs/PERFORMANCE_REPORT.md")
        perf_report_found = True
    else:
        print_error("Missing: PERFORMANCE_REPORT.md (required!)")
    
    checks.append(perf_report_found)
    
    # Optional test files
    print(f"\n{Colors.BOLD}Checking Test Files (Recommended):{Colors.END}")
    check_file_exists("tests/test_all_phases.py", required=False)
    
    return all(checks)


def validate_requirements():
    """Check that requirements.txt contains necessary dependencies"""
    print_header("DEPENDENCIES VALIDATION")
    
    if not Path("requirements.txt").exists():
        print_error("requirements.txt not found!")
        return False
    
    with open("requirements.txt", "r") as f:
        content = f.read().lower()
    
    required_packages = ["anytree"]
    missing = []
    
    for package in required_packages:
        if package in content:
            print_success(f"Found required package: {package}")
        else:
            print_error(f"Missing required package: {package}")
            missing.append(package)
    
    if missing:
        print(f"\n{Colors.YELLOW}Add these to requirements.txt:{Colors.END}")
        for pkg in missing:
            print(f"  {pkg}")
        return False
    
    return True


def validate_git_status():
    """Check Git status and remote setup"""
    print_header("GIT REPOSITORY VALIDATION")
    
    checks = []
    
    # Check if .git directory exists
    if not Path(".git").is_dir():
        print_error("Not a Git repository! Initialize with: git init")
        return False
    
    print_success("Git repository initialized")
    
    # Try to check git status
    try:
        import subprocess
        
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            if result.stdout.strip():
                print_warning("You have uncommitted changes!")
                print(f"\n{Colors.YELLOW}Uncommitted files:{Colors.END}")
                print(result.stdout)
                print(f"\n{Colors.YELLOW}Run: git add . && git commit -m 'Your message'{Colors.END}")
                checks.append(False)
            else:
                print_success("No uncommitted changes")
                checks.append(True)
        
        # Check remote
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            if result.stdout.strip():
                print_success("Git remote configured")
                print(f"\n{Colors.BOLD}Remote URL:{Colors.END}")
                print(result.stdout)
                checks.append(True)
            else:
                print_error("No Git remote configured!")
                print(f"\n{Colors.YELLOW}Run: git remote add origin <your-repo-url>{Colors.END}")
                checks.append(False)
        
        # Check if pushed
        result = subprocess.run(
            ["git", "log", "origin/main..HEAD"],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print_warning("You have unpushed commits!")
            print(f"\n{Colors.YELLOW}Run: git push origin main{Colors.END}")
            checks.append(False)
        elif result.returncode == 0:
            print_success("All commits pushed to remote")
            checks.append(True)
        
    except FileNotFoundError:
        print_error("Git command not found. Make sure Git is installed.")
        return False
    except Exception as e:
        print_warning(f"Could not fully validate Git status: {e}")
        return True  # Don't fail on git check issues
    
    return all(checks) if checks else True


def validate_readme_content():
    """Check that README contains essential information"""
    print_header("README VALIDATION")
    
    if not Path("README.md").exists():
        print_error("README.md not found!")
        return False
    
    with open("README.md", "r") as f:
        content = f.read().lower()
    
    checks = []
    
    # Check for essential sections
    essential_keywords = [
        ("project structure", "Project structure/organization"),
        ("setup", "Setup/installation instructions"),
        ("usage", "Usage/how to run"),
        ("phase", "Phase descriptions"),
    ]
    
    for keyword, description in essential_keywords:
        if keyword in content:
            print_success(f"Found section: {description}")
            checks.append(True)
        else:
            print_warning(f"Missing section: {description}")
            checks.append(False)
    
    return all(checks)


def print_submission_checklist():
    """Print the final submission checklist"""
    print_header("SUBMISSION CHECKLIST")
    
    checklist = [
        ("All source code files present", "Check file structure above"),
        ("GitHub repository created", "https://github.com/jagter4b/dsa-etl-project"),
        ("Collaborator 'hassaneldash' added", "Settings → Collaborators → Add people"),
        ("All changes committed", "git status should be clean"),
        ("All changes pushed to GitHub", "git push origin main"),
        ("Performance report completed", "PERFORMANCE_REPORT.md exists"),
        ("Email sent to hassanmeldash@gmail.com", "Use correct subject format below"),
    ]
    
    print("Review the following before final submission:\n")
    
    for i, (item, note) in enumerate(checklist, 1):
        print(f"{i}. [ ] {Colors.BOLD}{item}{Colors.END}")
        print(f"       {Colors.BLUE}→ {note}{Colors.END}\n")
    
    print(f"\n{Colors.BOLD}Email Subject Line (EXACT FORMAT):{Colors.END}")
    print(f"{Colors.GREEN}ITI PortSaid | PowerBI46R2 | DSA Project | DataFlow Pro | Group No.[X]{Colors.END}")
    print(f"{Colors.YELLOW}(Replace [X] with your actual group number){Colors.END}\n")


def main():
    """Main validation routine"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{'DataFlow Pro - Pre-Submission Validation':^70}{Colors.END}")
    print(f"{Colors.BOLD}{'ITI Port Said | PowerBI46R2':^70}{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    
    results = []
    
    # Run all validations
    results.append(("File Structure", validate_file_structure()))
    results.append(("Dependencies", validate_requirements()))
    results.append(("Git Repository", validate_git_status()))
    results.append(("README Content", validate_readme_content()))
    
    # Print summary
    print_header("VALIDATION SUMMARY")
    
    all_passed = True
    for name, passed in results:
        if passed:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
            all_passed = False
    
    print()
    
    # Print submission checklist
    print_submission_checklist()
    
    # Final message
    print_header("FINAL STATUS")
    
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 All automated checks PASSED!{Colors.END}")
        print(f"\n{Colors.GREEN}Your project appears ready for submission.{Colors.END}")
        print(f"{Colors.GREEN}Review the submission checklist above and submit when ready.{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠️  Some checks FAILED!{Colors.END}")
        print(f"\n{Colors.RED}Please fix the issues listed above before submitting.{Colors.END}")
        print(f"{Colors.RED}Re-run this script after making corrections.{Colors.END}\n")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Validation cancelled by user.{Colors.END}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}\n")
        sys.exit(1)
