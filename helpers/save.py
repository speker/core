# -*- coding: utf-8 -*-
import os


class Save:

    def to_disk(self, file_data, location, file_name, overwrite=False):
        directory_status = self.check_create_directory(location)
        if directory_status is not True:
            return False
        save_file_location = location + file_name
        try:
            if overwrite is False:
                f = open(save_file_location, 'wb')
                f.write(file_data)
            else:
                f = open(save_file_location, "wb+")
                f.write(file_data)
                f.close()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def check_create_directory(path):
        directory_paths = path.split('/')
        last_path = ''
        try:
            for dp in directory_paths:
                if len(dp) > 1:
                    dp = last_path + dp
                    last_path = dp + '/'
                    if os.path.exists(dp) is False:
                        os.mkdir(last_path)
                else:
                    last_path = '/'
        except Exception as e:
            print(e)
            return False
        return True
