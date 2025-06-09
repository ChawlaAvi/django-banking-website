#!/usr/bin/env python3
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import seaborn as sns

def fetch_all_commits(repo_owner, repo_name):
    """Fetch all commits from a GitHub repository"""
    commits = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        params = {
            'per_page': per_page,
            'page': page
        }
        
        print(f"Fetching page {page}...")
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
            
        page_commits = response.json()
        
        if not page_commits:
            break
            
        commits.extend(page_commits)
        page += 1
        
        # GitHub API rate limiting - be respectful
        if len(page_commits) < per_page:
            break
    
    return commits

def analyze_commits_by_author(commits):
    """Analyze commits by author"""
    author_stats = defaultdict(int)
    
    for commit in commits:
        author_name = commit['commit']['author']['name']
        author_stats[author_name] += 1
    
    return dict(author_stats)

def create_commit_plot(author_stats):
    """Create a bar plot of commits by author"""
    # Convert to DataFrame for easier plotting
    df = pd.DataFrame(list(author_stats.items()), columns=['Author', 'Commits'])
    df = df.sort_values('Commits', ascending=False)
    
    # Set up the plot
    plt.figure(figsize=(14, 8))
    
    # Create bar plot
    bars = plt.bar(range(len(df)), df['Commits'], color='skyblue', edgecolor='navy', alpha=0.7)
    
    # Customize the plot
    plt.title('Number of Commits by Author in AI Engineering Hub Repository', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Authors', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Commits', fontsize=12, fontweight='bold')
    
    # Set x-axis labels
    plt.xticks(range(len(df)), df['Author'], rotation=45, ha='right')
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('commits_by_author.png', dpi=300, bbox_inches='tight')
    plt.savefig('commits_by_author.pdf', bbox_inches='tight')
    
    return df

def print_summary(author_stats, total_commits):
    """Print a summary of the analysis"""
    print("\n" + "="*60)
    print("COMMIT ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total commits analyzed: {total_commits}")
    print(f"Number of unique contributors: {len(author_stats)}")
    print("\nTop 10 contributors:")
    print("-" * 40)
    
    sorted_authors = sorted(author_stats.items(), key=lambda x: x[1], reverse=True)
    for i, (author, count) in enumerate(sorted_authors[:10], 1):
        percentage = (count / total_commits) * 100
        print(f"{i:2d}. {author:<30} {count:4d} commits ({percentage:5.1f}%)")
    
    print("\n" + "="*60)

def main():
    repo_owner = "patchy631"
    repo_name = "ai-engineering-hub"
    
    print(f"Analyzing commits for {repo_owner}/{repo_name}...")
    
    # Fetch all commits
    commits = fetch_all_commits(repo_owner, repo_name)
    print(f"Fetched {len(commits)} commits")
    
    # Analyze commits by author
    author_stats = analyze_commits_by_author(commits)
    
    # Create visualization
    df = create_commit_plot(author_stats)
    
    # Print summary
    print_summary(author_stats, len(commits))
    
    # Save detailed data to CSV
    df.to_csv('commits_by_author.csv', index=False)
    print(f"\nDetailed data saved to 'commits_by_author.csv'")
    print(f"Plot saved as 'commits_by_author.png' and 'commits_by_author.pdf'")
    
    return df, author_stats

if __name__ == "__main__":
    df, stats = main()

