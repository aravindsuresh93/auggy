class EditAnnotations:
    def save(self):
        pass
    def rename(self,classes, old_name, new_name):
        if old_name not in classes['label'].unique():
            raise Exception("Label not found")
        classes['label'].replace({old_name:new_name}, inplace = True)
        self.save()
        
    def delete(self, classes, old_name):
        if old_name not in classes['label'].unique():
                raise Exception("Label not found")
        classes.loc[classes['label'] == old_name, 'deleted'] = True
