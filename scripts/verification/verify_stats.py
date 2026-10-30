import pandas as pd
from scipy import stats

df = pd.read_csv('data/raw/03_openrouter_outputs_v18_correct.csv')
greedy = df[df['purpose'] == 'greedy'].copy()
vce = df[df['purpose'] == 'vce'].copy()

# H1 numbers
af_acc = greedy[greedy['region'] == 'Africa']['correct'].mean()
eu_acc = greedy[greedy['region'] == 'Europe']['correct'].mean()
af_n = len(greedy[greedy['region'] == 'Africa'])
eu_n = len(greedy[greedy['region'] == 'Europe'])
af_correct = int(greedy[greedy['region'] == 'Africa']['correct'].sum())
eu_correct = int(greedy[greedy['region'] == 'Europe']['correct'].sum())
crosstab = pd.crosstab(greedy['region'], greedy['correct'])
chi2, p_chi2, dof, expected = stats.chi2_contingency(crosstab)

print(f'H1 Accuracy: Africa={af_acc:.3f} ({af_correct}/{af_n}), Europe={eu_acc:.3f} ({eu_correct}/{eu_n})')
print(f'H1 chi2={chi2:.3f}, p={p_chi2:.3f}')

# H2 CHR
high_conf = vce[vce['vce'] >= 0.70]
af_chr = (high_conf[(high_conf['region'] == 'Africa') & (high_conf['correct'] == 0)].shape[0] / 
          high_conf[high_conf['region'] == 'Africa'].shape[0])
eu_chr = (high_conf[(high_conf['region'] == 'Europe') & (high_conf['correct'] == 0)].shape[0] / 
          high_conf[high_conf['region'] == 'Europe'].shape[0])
print(f'H2 CHR: Africa={af_chr:.3f}, Europe={eu_chr:.3f}, ratio={af_chr/eu_chr:.3f}')

# H3 wrong-answer VCE
af_wrong = vce[(vce['region'] == 'Africa') & (vce['correct'] == 0)]['vce']
eu_wrong = vce[(vce['region'] == 'Europe') & (vce['correct'] == 0)]['vce']
print(f'H3 wrong-VCE: Africa={af_wrong.mean():.3f} (n={len(af_wrong)}), Europe={eu_wrong.mean():.3f} (n={len(eu_wrong)})')
