import pandas as pd
from sklearn.decomposition import PCA


def get_triplot_df_from_votes_df(votes_df):
    
    bdf = binarize_df(votes_df)

    votes_columns = [c for c in bdf.columns if c != 'bioguide']
    votes_only_df = bdf[votes_columns]
    bioguides_only_df = bdf[['bioguide']]
    
    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(votes_only_df)

    pdf = pd.DataFrame(data = principalComponents
                 , columns = ['pc1', 'pc2', 'pc3'])

    pdf = pdf.join(bioguides_only_df)
    
    return pdf