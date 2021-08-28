from utils.load_annotations import LoadAnnotations
from utils.save_annotations.save_pascal import save
LA = LoadAnnotations()
df, classes = LA.load("test/raw", ".xml", "test/raw", "test/yolo/classes.txt")

print(df)

save(df, classes, "/app/auggy/test/out")

