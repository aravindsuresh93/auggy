from utils.save_annotations.save_factory import SaveAnnotations


def save(df, classes, save_folder, format):
    saver = SaveAnnotations.get(format)
    ndf = df[df['deleted'] != False].copy()
    for filepath in ndf['path'].unique():
        sdf = ndf[ndf['path'] == filepath]
        info = list(sdf.to_dict(orient = 'index').values())
        if len(info):
            saver.save(info, classes, save_folder)

    if format in [".txt"]:
        saver.save_classes(classes, save_folder)
        