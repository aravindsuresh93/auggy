class Stats:
    def __init__(self, df, classes):
        self.df = df.copy()
        self.classes = classes.copy()
        
    def get_total_images(self):
            return len(self.df['image_path'].unique())

    def get_total_annotations(self):
            return len(self.df)

    def get_error_df(self):
        self.error_df = self.df[self.df['error']!=0]

    def get_total_errors(self):
            self.get_error_df()
            return len(self.error_df)

    def get_label_distribution(self):
        vc = self.df['label'].value_counts()
        vc = self.classes.merge(vc.to_frame(),  how='left', left_index = True, right_index=True)
        vc.columns = ["label", "count"]
        return vc.to_dict(orient = 'index')

    def get_global_stats(self):
        return {'total_images' : self.get_total_images(),
                'total_annotations' : self.get_total_annotations(),
                'total_errors' : self.get_total_errors(),
                'label_distribution' : self.get_label_distribution()
                }
        

    
