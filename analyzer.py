import json
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

print(*[filename.split(".")[0] for filename in os.listdir('opinions')])

product_code = input("Please enter product code: ")

opinions = pd.read_json(f"./opinions/{product_code}.json")


stars = opinions.stars.value_counts().reindex(list(np.arange(0.5,5.5,0.5)), fill_value=0)
stars.plot.bar()
for index, value in enumerate(stars):
    plt.text(index, value+1, str(value), ha='center')
plt.ylim([0, max(stars.values)*1.1])
plt.xticks(rotation=0)
plt.xlabel('Number of stars')
plt.ylabel('Number of opinions')
plt.grid(axis='y', which='major')

if not os.path.exists(f"./results"):
    os.mkdir(f"./results", mode=777)

plt.savefig(f'./results/{product_code} Stars.png')
plt.close()

recommendation = opinions.recommendation.value_counts(dropna=False).reindex([True, False, None])
recommendation.plot.pie(label="",
                        labels=["Recommended", "Not Recommended", "Neutral"],
                        colors= ['green', 'red', 'blue'],
                        autopct= lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '')
plt.savefig(f'./results/{product_code} Recommendations.png')

stats = {
    'opinions_count': len(opinions.index),
    'pros_count': int(opinions.pros.astype(bool).sum()),
    'cons_count': int(opinions.cons.astype(bool).sum()),
    'average_score': opinions.stars.mean().round(2),
    'stars': stars.to_dict(),
    'recommendations': recommendation.to_dict()
}

with open(f"./results/{product_code} Stats.json", "w", encoding="UTF-8") as file:
    json.dump(stats, file, indent=4, ensure_ascii=False)
print('Success')