from utils.load_annotations import LoadAnnotations
from utils.stats_annotation.get_stats import Stats
# from utils.save_annotations.save_pascal import save
LA = LoadAnnotations()
df, classes = LA.load("test/raw", ".xml", "test/raw", "test/yolo/classes.txt")

print(df)

stats = Stats(df, classes)
print(stats.get_global_stats())
print(stats.get_error_info())



# save(df, classes, "/app/auggy/test/out")
