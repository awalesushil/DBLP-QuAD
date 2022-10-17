import numpy as np
import matplotlib.pyplot as plt

from templates import templates

for entity in ["CREATOR", "PUBLICATION"]:
    print(f"Stats for Entity: {entity}")
    
    query_types = templates[entity].keys()
    total_templates = [len(templates[entity][each]) for each in query_types]
    weights = [len(templates[entity][each])/sum(total_templates) for each in query_types]

    print("Total number of templates:", sum(total_templates))
    print("Number of templates per query type:")
    for i, query_type in enumerate(query_types):
        print(f"{query_type}: {len(templates[entity][query_type])} ({weights[i]*100:.2f}%)")
    
    X_axis = np.arange(len(query_types))
    width = 0.4
    if entity == "CREATOR":
        creator = plt.bar(X_axis - 0.2, total_templates, width, label=entity)
    else:
        publication = plt.bar(X_axis + 0.2, total_templates, width, label=entity)

plt.bar_label(creator, padding=3)
plt.bar_label(publication, padding=3)
plt.xticks(X_axis, query_types)
plt.xlabel("Query Type")
plt.ylabel("Number of templates")
plt.title(f"Number of templates per query type")
plt.legend()
plt.show()