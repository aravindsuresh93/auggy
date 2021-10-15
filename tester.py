from utils.load_annotations import LoadAnnotations
from utils.stats_annotation.get_stats import Stats

from utils.edit_annotations import EditAnnotations
# from utils.save_annotations.save_pascal import save
LA = LoadAnnotations()
df, classes = LA.load("test/raw", ".xml", "test/raw", "test/yolo/classes.txt")

print(df, classes)


print('-'*100)

stats = Stats(df, classes)
print(stats.get_global_stats())
print(stats.get_error_info())

ea = EditAnnotations()
ea.rename(classes,'aravind','ad')
ea.delete(classes, 'dl')

print(classes)

print(stats.get_global_stats())



# save(df, classes, "/app/auggy/test/out")

