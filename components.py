import datetime
import os

class Components:
    def __init__(self):
        self.date = ""
        self.file_name = "things.txt"

        self.find_date_time()
        self.clean_file()

    def find_date_time(self):
        date_time = datetime.datetime.now()
        date_time_str = str(date_time)
        date = date_time_str.split(' ')[0]

        year = date.split('-')[0]
        month = date_time.strftime("%B")
        day = int(date.split('-')[2])
        self.date = f"{month} {day}, {year}"

    def clean_file(self):
        is_empty = self.is_file_empty()

        if is_empty:
            with open(self.file_name, 'a') as the_file:
                the_file.write(f'{self.date}\n')
        else:
            with open(self.file_name, "r") as a_file:
                date_correct = False

                for line in a_file:
                    if line == self.date:
                        date_corrrect = True

                if not date_correct:
                    with open(self.file_name, 'w') as f:
                        f.write(f'{self.date}\n')

    def is_file_empty(self):
        # Check if file exist and it is empty
        return os.path.exists(self.file_name) and os.stat(self.file_name).st_size == 0