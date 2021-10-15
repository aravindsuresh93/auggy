class Stats:
    def __init__(self, df, classes):
        self.df = df.copy()
        self.classes = classes.copy()
        
    def get_total_images(self):
            return len(self.df['image_path'].unique())

    def get_total_annotations(self):
            return len(self.df)

    def get_error_info(self):
        self.error_df = self.df[self.df['error']!=0]
        return {'count' : len(self.error_df), 
                'info' : self.error_df[['annotation_path', 'error']].to_dict(orient = 'index')}

    def get_label_distribution(self):
        vc = self.df['label'].value_counts()
        vc = self.classes.merge(vc.to_frame(),  how='left', left_index = True, right_index=True)
        vc.columns = ["label", "deleted", "count"]
        return vc[vc['deleted'] != True][["label",  "count"]].to_dict(orient = 'index')

    @staticmethod
    def check_leak(row):
        soft_error  = ""
        xmin, xmax, ymin, ymax, height, width = row['xmin'], row['xmax'], row['ymin'], row['ymax'], row['height'], row['width']
        if xmin < 0 or ymin < 0 or xmax < 0 or ymax < 0:
            soft_error = "Bounding box co-ordintes less than 0" 
        if xmin > width or ymin > height or xmax > width or ymax > height:
            soft_error = "Bounding box co-ordinates exceeds image dimensions"
        return soft_error if len(soft_error) else False

    def get_bounding_box_leak_info(self):
        self.df['soft_error'] = self.df.apply(lambda row : Stats.check_leak(row),1)
        ret = self.df[self.df['soft_error'] != False].to_dict(orient = 'index')
        return {'count' : len(ret), 
                'info' : ret}

    def get_global_stats(self):
        return {'total_images' : self.get_total_images(),
                'total_annotations' : self.get_total_annotations(),
                'total_errors' : self.get_error_info(),
                'bounding_box_leak' : self.get_bounding_box_leak_info(),
                'label_distribution' : self.get_label_distribution()
                }
        
    
    
