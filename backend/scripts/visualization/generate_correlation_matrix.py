import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Arial'


# Add backend root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(backend_dir)

from app.database import SessionLocal
from app.models import Place, Category, InteractionLog

def generate_corr_matrix():
    db = SessionLocal()
    
    places = db.query(Place).all()
    
    # We want to build a dataset of places to see feature correlations
    data = []
    
    for p in places:
        # Get category parent_type
        cat_type = p.category.parent_type if p.category else 'other'
        
        row = {
            'Latitude': float(p.location_lat) if p.location_lat else 0.0,
            'Longitude': float(p.location_lng) if p.location_lng else 0.0,
            'Average Rating': float(p.rating_avg) if p.rating_avg else 0.0,
            'Is Nature': 1 if cat_type == 'nature' else 0,
            'Is Culture': 1 if cat_type == 'culture' else 0,
            'Is Cafe': 1 if cat_type == 'cafe' else 0,
            'Is Local Food': 1 if cat_type == 'local_food' else 0,
            'Is Landmark': 1 if cat_type == 'landmark' else 0,
            'Is Chill': 1 if cat_type == 'chill' else 0,
        }
        
        # Also let's get interaction count for popularity
        interaction_count = db.query(InteractionLog).filter(InteractionLog.place_id == p.id).count()
        row['Popularity (Interactions)'] = interaction_count
        
        data.append(row)
        
    db.close()
    
    if not data:
        print("No data available to generate correlation matrix.")
        return
        
    df = pd.DataFrame(data)

    # Compute the correlation matrix
    corr = df.corr()

    # ============================================================
    # Plot — academic document style
    # ============================================================
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap='coolwarm',
        vmin=-1, vmax=1,
        linewidths=0.5,
        linecolor='#dddddd',
        cbar_kws={"shrink": 0.8},
        annot_kws={"size": 10},
        ax=ax
    )

    ax.set_title('Feature Correlation Matrix (Place Attributes & Interactions)',
                 fontsize=13, fontweight='normal', pad=12)
    ax.tick_params(axis='x', labelsize=10, rotation=45)
    ax.tick_params(axis='y', labelsize=10, rotation=0)
    plt.xticks(ha='right')

    plt.tight_layout()
    plots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    output_path = os.path.join(plots_dir, 'place_correlation_matrix.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Successfully saved: {output_path}")

if __name__ == '__main__':
    generate_corr_matrix()
