# https://stackoverflow.com/questions/15535655/optional-arguments-in-initializer-of-python-class

import pandas as pd


class ProcessedData:


    def __init__(self, df=None, url=None):
        self.df = df
        self.url = url
        self.cleaned_data = None
        self.gendered_data = None

        if url is not None:
            self.df = pd.read_csv(url, header=0, index_col=None)

    # create class methods
    @classmethod
    def determine_agegroup(cls, row):
        start_ages = [10, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
        end_ages = [17, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 100]
        age = int(row['Age'])
        for start, stop in zip(start_ages, end_ages):
            if start <= age <= stop:
                return '%d-%d' % (start, stop)

    @staticmethod
    def get_piechart_data(df):
        datapie = df
        datapie['Age Group'] = datapie.apply(ProcessedData.determine_agegroup, axis=1)
        return datapie

    def get_cleaned_data(self, cuttoff_year=1):
        self.cleaned_data = self.df[self.df['Age'] > cuttoff_year]
        return self.cleaned_data

    def get_gendered_data(self, gender, cuttoff_year=1):
        self.gendered_data = self.get_cleaned_data(cuttoff_year)
        self.gendered_data = self.gendered_data[self.gendered_data['Gender'] == gender]
        return self.gendered_data

