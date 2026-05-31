"""
Indian Language Similarity Network
===================================
A computational study analyzing phonological similarities between Indian languages
using PHOIBLE 2.0 data. Builds a similarity network, performs community detection,
and compares computational clusters with known language families.

Author: Mandavi Singh
Date: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

PHOIBLE_URL = 'https://raw.githubusercontent.com/phoible/dev/master/data/phoible.csv'
GLOTTOLOG_URL = 'https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/languages.csv'

OUTPUT_DIR = './'

# India bounding box
INDIA_LAT_MIN, INDIA_LAT_MAX = 6.0, 37.0
INDIA_LON_MIN, INDIA_LON_MAX = 68.0, 97.0


# Family color mapping
FAMILY_COLORS = {
    'Indo-Aryan': '#1565C0',
    'Dravidian': '#2E7D32',
    'Austroasiatic': '#E65100',
    'Tibeto-Burman': '#7B1FA2',
    'Other': '#546E7A',
}

# Known Indian language family mappings (Glottolog Family_ID -> Simple name)
FAMILY_MAPPING = {
    'indo1319': 'Indo-Aryan',
    'drav1251': 'Dravidian',
    'aust1305': 'Austroasiatic',
    'sino1245': 'Tibeto-Burman',
}

plt.rcParams.update({
    'figure.figsize': (14, 10),
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
})
sns.set_theme(style='whitegrid', font_scale=1.05)



# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================

def load_data():
    """Load PHOIBLE and Glottolog datasets."""
    print("=" * 60)
    print("STEP 1: Loading Data")
    print("=" * 60)

    # Load PHOIBLE
    try:
        phoible = pd.read_csv(PHOIBLE_URL, low_memory=False)
        print(f"  PHOIBLE loaded: {phoible.shape[0]:,} rows, {phoible.shape[1]} columns")
    except Exception as e:
        print(f"  PHOIBLE download failed: {e}")
        phoible = pd.read_csv('../phoible.csv', low_memory=False)
        print(f"  PHOIBLE loaded from local: {phoible.shape[0]:,} rows")

    # Load Glottolog
    try:
        glottolog = pd.read_csv(GLOTTOLOG_URL, low_memory=False)
        glottolog = glottolog[['ID', 'Name', 'Latitude', 'Longitude', 'Macroarea', 'Family_ID']]
        glottolog = glottolog.dropna(subset=['Latitude', 'Longitude'])
        glottolog = glottolog.rename(columns={'ID': 'Glottocode', 'Name': 'GlottoName'})
        print(f"  Glottolog loaded: {len(glottolog):,} languages with coordinates")
    except Exception as e:
        raise RuntimeError(f"  Glottolog download failed: {e}")

    return phoible, glottolog



# ============================================================================
# STEP 2: FILTER INDIAN LANGUAGES & BUILD PHONEME VECTORS
# ============================================================================

def filter_indian_languages(phoible, glottolog):
    """Filter to Indian languages and build phoneme feature vectors."""
    print("\n" + "=" * 60)
    print("STEP 2: Filtering Indian Languages")
    print("=" * 60)

    # Filter Glottolog for India region
    india_glotto = glottolog[
        (glottolog['Latitude'] >= INDIA_LAT_MIN) &
        (glottolog['Latitude'] <= INDIA_LAT_MAX) &
        (glottolog['Longitude'] >= INDIA_LON_MIN) &
        (glottolog['Longitude'] <= INDIA_LON_MAX)
    ].copy()
    print(f"  Languages in India bounding box: {len(india_glotto)}")

    # Map families
    india_glotto['Family_Name'] = india_glotto['Family_ID'].map(FAMILY_MAPPING).fillna('Other')
    print(f"  Family distribution:")
    print(india_glotto['Family_Name'].value_counts().to_string(header=False))

    # Merge with PHOIBLE - get phoneme inventories
    phoible_india = phoible[
        phoible['Glottocode'].isin(india_glotto['Glottocode'])
    ].copy()
    print(f"\n  PHOIBLE rows for Indian languages: {len(phoible_india):,}")

    # Keep only consonants and vowels
    phoneme_data = phoible_india[
        phoible_india['SegmentClass'].isin(['vowel', 'consonant'])
    ].copy()


    # One inventory per language (choose the largest)
    inv_sizes = phoneme_data.groupby(['Glottocode', 'InventoryID'])['Phoneme'].nunique().reset_index()
    inv_sizes.columns = ['Glottocode', 'InventoryID', 'Size']
    best_inv = inv_sizes.sort_values('Size', ascending=False).groupby('Glottocode').first().reset_index()

    # Filter to best inventory per language
    phoneme_data = phoneme_data.merge(
        best_inv[['Glottocode', 'InventoryID']],
        on=['Glottocode', 'InventoryID'],
        how='inner'
    )

    # Get unique languages
    languages = phoneme_data.groupby('Glottocode').agg(
        LanguageName=('LanguageName', 'first'),
    ).reset_index()

    # Merge with family info
    languages = languages.merge(
        india_glotto[['Glottocode', 'Family_Name', 'Latitude', 'Longitude']],
        on='Glottocode', how='inner'
    ).drop_duplicates(subset='Glottocode')

    print(f"\n  Final Indian languages with phoneme data: {len(languages)}")
    print(f"  Family breakdown:")
    for fam, count in languages['Family_Name'].value_counts().items():
        print(f"    {fam}: {count}")

    return phoneme_data, languages, india_glotto



# ============================================================================
# STEP 3: COMPUTE SIMILARITY MATRIX (Jaccard Similarity)
# ============================================================================

def compute_similarity_matrix(phoneme_data, languages):
    """Compute Jaccard similarity between all language pairs."""
    print("\n" + "=" * 60)
    print("STEP 3: Computing Phonological Similarity Matrix")
    print("=" * 60)

    # Build binary phoneme presence matrix
    # Rows = languages, Columns = phonemes (1 if present, 0 if not)
    lang_phonemes = {}
    for glottocode in languages['Glottocode'].values:
        phonemes = set(
            phoneme_data[phoneme_data['Glottocode'] == glottocode]['Phoneme'].unique()
        )
        lang_phonemes[glottocode] = phonemes

    # Get all unique phonemes across Indian languages
    all_phonemes = sorted(set().union(*lang_phonemes.values()))
    print(f"  Total unique phonemes across Indian languages: {len(all_phonemes)}")

    # Build binary matrix
    glottocodes = languages['Glottocode'].values
    n_langs = len(glottocodes)
    binary_matrix = np.zeros((n_langs, len(all_phonemes)), dtype=int)

    for i, gc in enumerate(glottocodes):
        for j, ph in enumerate(all_phonemes):
            if ph in lang_phonemes[gc]:
                binary_matrix[i, j] = 1

    print(f"  Binary matrix shape: {binary_matrix.shape}")
    print(f"  Mean phonemes per language: {binary_matrix.sum(axis=1).mean():.1f}")


    # Compute Jaccard distance matrix
    jaccard_distances = squareform(pdist(binary_matrix, metric='jaccard'))
    # Convert to similarity
    similarity_matrix = 1 - jaccard_distances

    print(f"  Similarity matrix shape: {similarity_matrix.shape}")
    print(f"  Mean pairwise similarity: {similarity_matrix[np.triu_indices(n_langs, k=1)].mean():.3f}")
    print(f"  Max similarity: {similarity_matrix[np.triu_indices(n_langs, k=1)].max():.3f}")
    print(f"  Min similarity: {similarity_matrix[np.triu_indices(n_langs, k=1)].min():.3f}")

    return binary_matrix, similarity_matrix, all_phonemes



# ============================================================================
# STEP 4: BUILD NETWORK GRAPH
# ============================================================================

def build_network(similarity_matrix, languages, threshold=0.5):
    """Build a network graph from similarity matrix."""
    print("\n" + "=" * 60)
    print(f"STEP 4: Building Network (threshold = {threshold})")
    print("=" * 60)

    G = nx.Graph()
    glottocodes = languages['Glottocode'].values
    n = len(glottocodes)

    # Add nodes with attributes
    for i, row in languages.iterrows():
        G.add_node(row['Glottocode'],
                   label=row['LanguageName'],
                   family=row['Family_Name'],
                   lat=row['Latitude'],
                   lon=row['Longitude'])

    # Add edges where similarity > threshold
    edge_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            sim = similarity_matrix[i, j]
            if sim >= threshold:
                G.add_edge(glottocodes[i], glottocodes[j], weight=sim)
                edge_count += 1

    print(f"  Nodes: {G.number_of_nodes()}")
    print(f"  Edges: {G.number_of_edges()}")
    print(f"  Density: {nx.density(G):.4f}")
    print(f"  Connected components: {nx.number_connected_components(G)}")

    return G



# ============================================================================
# STEP 5: COMMUNITY DETECTION
# ============================================================================

def detect_communities(G, languages):
    """Detect communities using Louvain method and compare with families."""
    print("\n" + "=" * 60)
    print("STEP 5: Community Detection (Louvain)")
    print("=" * 60)

    # Use greedy modularity (built into networkx)
    communities = list(nx.community.greedy_modularity_communities(G, weight='weight'))

    print(f"  Communities detected: {len(communities)}")
    print(f"  Modularity: {nx.community.modularity(G, communities, weight='weight'):.4f}")

    # Assign community labels
    community_map = {}
    for i, comm in enumerate(communities):
        for node in comm:
            community_map[node] = i

    # Add community to languages df
    languages = languages.copy()
    languages['Community'] = languages['Glottocode'].map(community_map)

    # Compare communities with families
    print("\n  Community vs Family composition:")
    for i, comm in enumerate(communities):
        comm_langs = languages[languages['Glottocode'].isin(comm)]
        family_counts = comm_langs['Family_Name'].value_counts()
        print(f"\n    Community {i} ({len(comm)} languages):")
        for fam, cnt in family_counts.items():
            print(f"      {fam}: {cnt}")

    return communities, community_map, languages



# ============================================================================
# STEP 6: VISUALIZATIONS
# ============================================================================

def visualize_network(G, languages, communities, community_map):
    """Create network visualization colored by language family."""
    print("\n" + "=" * 60)
    print("STEP 6: Generating Visualizations")
    print("=" * 60)

    # --- Plot 1: Network colored by FAMILY ---
    fig, axes = plt.subplots(1, 2, figsize=(20, 9))

    # Layout
    pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42, weight='weight')

    # Colors by family
    node_colors_family = []
    for node in G.nodes():
        fam = G.nodes[node].get('family', 'Other')
        node_colors_family.append(FAMILY_COLORS.get(fam, '#546E7A'))

    # Draw network - by family
    ax = axes[0]
    nx.draw_networkx_edges(G, pos, alpha=0.08, width=0.5, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors_family,
                           node_size=80, alpha=0.85, ax=ax)

    # Legend
    legend_patches = [mpatches.Patch(color=c, label=f) for f, c in FAMILY_COLORS.items()]
    ax.legend(handles=legend_patches, loc='upper left', fontsize=9)
    ax.set_title('Indian Language Similarity Network\n(colored by Language Family)',
                 fontsize=13, fontweight='bold')
    ax.axis('off')


    # --- Plot 2: Network colored by COMMUNITY ---
    n_communities = len(communities)
    community_colors_map = plt.cm.Set3(np.linspace(0, 1, max(n_communities, 3)))

    node_colors_comm = []
    for node in G.nodes():
        comm_id = community_map.get(node, 0)
        node_colors_comm.append(community_colors_map[comm_id % len(community_colors_map)])

    ax = axes[1]
    nx.draw_networkx_edges(G, pos, alpha=0.08, width=0.5, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors_comm,
                           node_size=80, alpha=0.85, ax=ax)

    comm_patches = [mpatches.Patch(color=community_colors_map[i],
                    label=f'Community {i}') for i in range(n_communities)]
    ax.legend(handles=comm_patches, loc='upper left', fontsize=9)
    ax.set_title('Indian Language Similarity Network\n(colored by Detected Community)',
                 fontsize=13, fontweight='bold')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}network_family_vs_community.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: network_family_vs_community.png")


    # --- Plot 3: Similarity Heatmap ---
    fig, ax = plt.subplots(figsize=(14, 12))

    # Sort languages by family for better visualization
    lang_sorted = languages.sort_values(['Family_Name', 'LanguageName']).reset_index(drop=True)
    sorted_indices = [list(languages['Glottocode']).index(gc) for gc in lang_sorted['Glottocode']]
    sim_sorted = similarity_matrix[np.ix_(sorted_indices, sorted_indices)]

    # Create labels with family prefix
    labels = [f"{row['LanguageName'][:15]}" for _, row in lang_sorted.iterrows()]

    sns.heatmap(sim_sorted, xticklabels=labels, yticklabels=labels,
                cmap='YlOrRd', vmin=0, vmax=1, ax=ax,
                cbar_kws={'label': 'Jaccard Similarity'})
    ax.set_title('Phonological Similarity Heatmap\n(Indian Languages, sorted by family)',
                 fontsize=14, fontweight='bold')
    plt.xticks(fontsize=5, rotation=90)
    plt.yticks(fontsize=5)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}similarity_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: similarity_heatmap.png")


    # --- Plot 4: Dendrogram (Hierarchical Clustering) ---
    fig, ax = plt.subplots(figsize=(18, 8))

    # Use Jaccard distance for linkage
    condensed_dist = pdist(binary_matrix, metric='jaccard')
    Z = linkage(condensed_dist, method='ward')

    # Color by family
    lang_names = [languages.iloc[i]['LanguageName'][:20] for i in range(len(languages))]

    dendrogram(Z, labels=lang_names, leaf_rotation=90, leaf_font_size=6, ax=ax)
    ax.set_title('Hierarchical Clustering of Indian Languages\n(Ward linkage on Jaccard distance)',
                 fontsize=14, fontweight='bold')
    ax.set_ylabel('Distance')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}dendrogram.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: dendrogram.png")


    # --- Plot 5: Inter/Intra family similarity boxplot ---
    fig, ax = plt.subplots(figsize=(12, 6))

    intra_sims = {fam: [] for fam in FAMILY_COLORS.keys()}
    inter_sims = []

    glottocodes = list(languages['Glottocode'])
    families = list(languages['Family_Name'])
    n = len(glottocodes)

    for i in range(n):
        for j in range(i + 1, n):
            sim = similarity_matrix[i, j]
            if families[i] == families[j]:
                fam = families[i]
                if fam in intra_sims:
                    intra_sims[fam].append(sim)
            else:
                inter_sims.append(sim)

    # Box plot
    data_to_plot = []
    labels_to_plot = []
    for fam in ['Indo-Aryan', 'Dravidian', 'Austroasiatic', 'Tibeto-Burman']:
        if intra_sims[fam]:
            data_to_plot.append(intra_sims[fam])
            labels_to_plot.append(f'{fam}\n(intra)')
    data_to_plot.append(inter_sims)
    labels_to_plot.append('Inter-family')

    bp = ax.boxplot(data_to_plot, labels=labels_to_plot, patch_artist=True)
    colors = ['#1565C0', '#2E7D32', '#E65100', '#7B1FA2', '#90A4AE']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax.set_ylabel('Jaccard Similarity')
    ax.set_title('Intra-Family vs Inter-Family Phonological Similarity',
                 fontsize=13, fontweight='bold')
    ax.axhline(y=np.mean(inter_sims), color='red', linestyle='--', alpha=0.5,
               label=f'Inter-family mean: {np.mean(inter_sims):.3f}')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}intra_vs_inter_similarity.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: intra_vs_inter_similarity.png")

    return intra_sims, inter_sims



# ============================================================================
# STEP 7: GENERATE REPORT
# ============================================================================

def generate_report(languages, similarity_matrix, G, communities, intra_sims, inter_sims):
    """Print analysis report with key findings."""
    print("\n" + "=" * 60)
    print("STEP 7: KEY FINDINGS")
    print("=" * 60)

    n = len(languages)
    upper_tri = similarity_matrix[np.triu_indices(n, k=1)]

    print(f"\n  Dataset:")
    print(f"    Indian languages analyzed: {n}")
    print(f"    Language families: {languages['Family_Name'].nunique()}")

    print(f"\n  Network Statistics:")
    print(f"    Nodes: {G.number_of_nodes()}")
    print(f"    Edges: {G.number_of_edges()}")
    print(f"    Density: {nx.density(G):.4f}")
    print(f"    Connected components: {nx.number_connected_components(G)}")
    print(f"    Communities detected: {len(communities)}")
    mod = nx.community.modularity(G, communities, weight='weight')
    print(f"    Modularity: {mod:.4f}")

    print(f"\n  Similarity Statistics:")
    print(f"    Mean pairwise similarity: {upper_tri.mean():.4f}")
    print(f"    Std: {upper_tri.std():.4f}")
    print(f"    Max: {upper_tri.max():.4f}")
    print(f"    Min: {upper_tri.min():.4f}")

    print(f"\n  Intra-Family vs Inter-Family:")
    for fam in ['Indo-Aryan', 'Dravidian', 'Austroasiatic', 'Tibeto-Burman']:
        if intra_sims[fam]:
            mean_s = np.mean(intra_sims[fam])
            print(f"    {fam} (intra): mean = {mean_s:.4f}, n_pairs = {len(intra_sims[fam])}")
    print(f"    Inter-family: mean = {np.mean(inter_sims):.4f}, n_pairs = {len(inter_sims)}")

    # Key finding: are intra > inter?
    all_intra = []
    for v in intra_sims.values():
        all_intra.extend(v)
    if all_intra:
        from scipy.stats import mannwhitneyu
        stat, pval = mannwhitneyu(all_intra, inter_sims, alternative='greater')
        print(f"\n  Mann-Whitney U (intra > inter): U = {stat:.0f}, p = {pval:.6f}")
        if pval < 0.05:
            print("    --> SIGNIFICANT: Languages within the same family are more")
            print("        phonologically similar than languages from different families.")
        else:
            print("    --> Not significant at p < 0.05")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)



# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Step 1: Load data
    phoible, glottolog = load_data()

    # Step 2: Filter Indian languages
    phoneme_data, languages, india_glotto = filter_indian_languages(phoible, glottolog)

    # Step 3: Compute similarity matrix
    binary_matrix, similarity_matrix, all_phonemes = compute_similarity_matrix(phoneme_data, languages)

    # Step 4: Build network (threshold = 0.45 for good connectivity)
    G = build_network(similarity_matrix, languages, threshold=0.45)

    # Step 5: Community detection
    communities, community_map, languages = detect_communities(G, languages)

    # Step 6: Visualizations
    intra_sims, inter_sims = visualize_network(G, languages, communities, community_map)

    # Step 7: Report
    generate_report(languages, similarity_matrix, G, communities, intra_sims, inter_sims)

    print("\nAll outputs saved to:", OUTPUT_DIR)
