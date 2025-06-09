import matplotlib.pyplot as plt
import pandas as pd

# Data from the analysis
data = {
    'Author': ['patchy631', 'Akshay Pachaar', 'Avi Chawla', 'nikhil-1e9', 'Sitam Meur', 
               'Nikhil Kotra', 'Gianpaolo Macario', 'Others (6 contributors)'],
    'Commits': [138, 46, 44, 11, 7, 4, 4, 7]  # Others = sum of remaining 6 contributors
}

df = pd.DataFrame(data)

# Create a more compact horizontal bar chart
plt.figure(figsize=(12, 8))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

bars = plt.barh(df['Author'], df['Commits'], color=colors)

# Customize the plot
plt.title('AI Engineering Hub Repository - Commits by Author', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Commits', fontsize=12, fontweight='bold')
plt.ylabel('Contributors', fontsize=12, fontweight='bold')

# Add value labels on the bars
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width + 1, bar.get_y() + bar.get_height()/2, 
             f'{int(width)}', ha='left', va='center', fontweight='bold')

# Add grid for better readability
plt.grid(axis='x', alpha=0.3, linestyle='--')

# Invert y-axis to show highest contributor at top
plt.gca().invert_yaxis()

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('ai_hub_commits_horizontal.png', dpi=300, bbox_inches='tight')
plt.show()

print("Horizontal bar chart saved as 'ai_hub_commits_horizontal.png'")

