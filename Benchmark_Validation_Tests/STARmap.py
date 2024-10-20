import warnings
warnings.filterwarnings('ignore')
import numpy as np
import SpaceFlow
import scanpy as sc
import pandas as pd
import os
import sys
from MCSER_SpaceFlow import MCSER_SpaceFlow
import matplotlib.pyplot as plt
from sklearn.metrics.cluster import normalized_mutual_info_score

#For STARmap, we combine topological features with the SpaceFlow embedding
section_id = sys.argv[1]
adata = sc.read('./Data/STARmap/'+section_id+'.h5ad')

#Validation
nmi_list=[1,2,3,4,5,6,7,8,9,10]

for i in range(10):
    adata2 = adata.copy()
    n = adata2.obs['label'].nunique()
    adata2 = MCSER_SpaceFlow(adata = adata2, n_clusters = n)

    NMI = normalized_mutual_info_score(adata2.obs['MCSER_spatial_domains'].values,  adata2.obs['label'].values)
    print('MCSER NMI = %.5f' %NMI)
    nmi_list[i] = NMI
    if i == 1:
        plt.rcParams["figure.figsize"] = (8, 8)
        sc.pl.spatial(adata2, color='mclust', cmap = 'tab20', save=section_id+'_tast.png', spot_size=150)

mean = np.mean(nmi_list)
print('Average MCSER NMI:', mean)

#Write results to CSV for easy check
results = {
        'Dataset': [section_id],
        'MCSER NMI': [mean]
    }
results_df = pd.DataFrame(results)
file_path = 'collected_results.csv'
file_exists = os.path.exists(file_path)
results_df.to_csv(file_path, mode='a', index=False, header=not file_exists)
