import warnings
import pandas as pd
from sdv.evaluation import evaluate

from sdv.metrics.tabular import BinaryDecisionTreeClassifier, BinaryAdaBoostClassifier,\
    BinaryLogisticRegression, BinaryMLPClassifier, BNLikelihood, LogisticDetection,\
    CSTest, KSTest

"""
Evaluation of datasets generated by the model
"""

# Ingore pandas and python warnings
warnings.filterwarnings('ignore')
pd.options.mode.chained_assignment = None


def print_similarity(title, fsp_fn, fup_fn, ssp_fn, sup_fn):
    """Compute various metrics to evaluate the generated datasets.

    Args:
        title (str):
            Info about the dataset and training.
        fsp_fn (str):
            Fake seen patients dataset (generated from the ontology).
        fup_fn (str):
            Fake unseen patients dataset (generated from the ontology).
        ssp_fn (str):
            Sampled seen patients dataset (sampled from the model).
        sup_fn (str):
            Sampled unseen patients dataset (sampled from the model).
    """
    sampled_seen_patients = pd.read_csv(ssp_fn)
    sampled_seen_patients.drop(columns=sampled_seen_patients.columns[0], axis=1, inplace=True)
    sampled_unseen_patients = pd.read_csv(sup_fn)
    sampled_unseen_patients.drop(columns=sampled_unseen_patients.columns[0], axis=1, inplace=True)
    fake_seen_patients = pd.read_csv(fsp_fn)
    fake_unseen_patients = pd.read_csv(fup_fn)
    # Aligning the fake unseen datasets' columns with the columns of the unseen sampled dataset
    fake_unseen_patients = fake_unseen_patients[sampled_unseen_patients.columns]

    print(f'Results for {title}')
    print(f'Fake Seen Patients: {len(fake_seen_patients)}x{len(fake_seen_patients.columns)} Fake Unseen Patients: {len(fake_unseen_patients)}x{len(fake_unseen_patients.columns)} Sampled Seen Patients: {len(sampled_seen_patients)}x{len(sampled_seen_patients.columns)} Sampled Unseen Patients: {len(sampled_unseen_patients)}x{len(sampled_unseen_patients.columns)}')
    print(f'Similarity between fake and sampled seen patients data: {evaluate(fake_seen_patients, sampled_seen_patients):.3f}')
    print(f'Similarity between fake and sampled unseen patients data: {evaluate(fake_unseen_patients, sampled_unseen_patients):.3f}')

    for (text, fp, sp) in [('Seen', fake_seen_patients, sampled_seen_patients), ('Unseen', fake_unseen_patients, sampled_unseen_patients)]:
        print(f"CSTest, {text}: {CSTest.compute(fp, sp):.3f}")
        print(f"KSTest, {text}: {KSTest.compute(fp, sp):.3f}")
        print(f"BDT, {text}: {BinaryDecisionTreeClassifier.compute(fp, sp, target='rare_disease'):.3f}")
        print(f"Ada, {text}: {BinaryAdaBoostClassifier.compute(fp, sp, target='rare_disease'):.3f}")
        print(f"LR, {text}: {BinaryLogisticRegression.compute(fp, sp, target='rare_disease'):.3f}")
        print(f"MLP, {text}: {BinaryMLPClassifier.compute(fp, sp, target='rare_disease'):.3f}")
        # print(f"BN, {text}: {BNLikelihood.compute(fp, sp):.3f}")
        print(f"LD, {text}: {LogisticDetection.compute(fp, sp):.3f}")

    print('')  # line break


print_similarity(title='Brain and lung RDs, 100x50 dataset, 5000 epochs',
                 fsp_fn='../persistent/data/syn_data/syn_patients_data_seen_100_50_brain_lung.csv',
                 fup_fn='../persistent/data/syn_data/syn_patients_data_unseen_100_50_brain_lung (353).csv',
                 ssp_fn='../persistent/model/brain_lung_100_50_seen_sample_100_rows.csv',
                 sup_fn='../persistent/model/brain_lung_100_50_unseen_sample_100_rows.csv'
                )

print_similarity(title='Leukemia RDs, 600x50 dataset, 5000 epochs',
                 fsp_fn='../persistent/data/syn_data/syn_patients_data_seen_600_50_leukemia.csv',
                 fup_fn='../persistent/data/syn_data/syn_patients_data_unseen_150_50_leukemia.csv',
                 ssp_fn='../persistent/model/2022_08_23_13_23_06_seen_sample_600_rows.csv',
                 sup_fn='../persistent/model/2022_08_23_13_23_06_unseen_sample_600_rows.csv'
                )

print_similarity(title='Leukemia RDs, 600x50 dataset, 10000 epochs',
                 fsp_fn='../persistent/data/syn_data/syn_patients_data_seen_600_50_leukemia.csv',
                 fup_fn='../persistent/data/syn_data/syn_patients_data_unseen_150_50_leukemia.csv',
                 ssp_fn='../persistent/model/leukemia_600_50_10000_epochs_seen_sample_600_rows.csv',
                 sup_fn='../persistent/model/leukemia_600_50_10000_epochs_unseen_sample_600_rows.csv'
                )