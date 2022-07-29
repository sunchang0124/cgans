from dp_cgans import DP_CGAN, Onto_DP_CGAN, OntologyEmbedding
import pandas as pd
import os
import numpy as np


result_samples_path = '../persistent/model'
if not os.path.exists(result_samples_path):
    os.makedirs(result_samples_path)

tabular_data = pd.read_csv("../persistent/data/syn_data/syn_patients_data_selected.csv", header=0)

col = tabular_data.columns
col_to_del = []
for c in col:
    if len(tabular_data[c].unique()) < 2:
        col_to_del.append(c)
tabular_data = tabular_data.drop(col_to_del, axis=1)


columns = tabular_data.columns.values.tolist()
# del columns[0]  # deleting patient_id column name

onto_embedding = OntologyEmbedding(embedding_path='../persistent/data/ontology/embeddings/hp_hoom_ordo_10/ontology.embeddings',
                                   embedding_size=100,
                                   hp_dict_fn='../persistent/data/ontology/HPO.dict',
                                   rd_dict_fn='../persistent/data/ontology/ORDO.dict')

# We adjusted the original CTGAN model from SDV. Instead of looking at the distribution of individual variable, we extended to two variables and keep their corrll
model = Onto_DP_CGAN(
    embedding=onto_embedding,
    columns=columns,
    sample_epochs=100,
    sample_epochs_path=result_samples_path,
    log_file_path=result_samples_path,
    # primary_key='patient_id',
    epochs=2, # number of training epochs
    batch_size=1000, # the size of each batch
    log_frequency=True,
    verbose=True,
    noise_dim=100,
    generator_dim=(128, 128, 128),
    discriminator_dim=(128, 128, 128),
    generator_lr=2e-4,
    discriminator_lr=2e-4,
    discriminator_steps=1,
    private=False,
)

print("Start model training")
model.fit(tabular_data)

print('Training finished, saving the model')
model.save('../persistent/model/onto_dp_cgans_model.pkl')

# Sample the generated synthetic data
nb_rows = 100
model.sample(nb_rows).to_csv(os.path.join(result_samples_path, f'final_sample_{nb_rows}_rows.csv'))
