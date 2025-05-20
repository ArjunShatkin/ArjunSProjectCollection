
import pandas as pd
import sankey as sk

class AllStarAPI:
    def load_gad(self, filename):
        # load the gad and clean the data as needed for our final visualization
        self.df = pd.read_csv(filename) # our dataframe (database) - STATE VARIABLE
        
        # data cleaning steps:
        self.df['yearID'] = self.df['yearID'].astype(int)
        self.df['decade'] = (self.df['yearID'] // 10) * 10
        self.df.loc[(self.df['startingPos'] > 1) & (self.df['startingPos'] < 7), 'positionType'] = 'Infielder'
        self.df.loc[self.df['startingPos'] > 6, 'positionType'] = 'Outfielder'
        self.df.loc[self.df['startingPos'] == 1, 'positionType'] = 'Pitcher'
        self.df = self.df[['positionType','decade','teamID']]

        # drop rows with n/a values
        self.df = self.df.dropna()

    def extract_network(self, min_connections,src_col,targ_col):
        # use group by the count the number of connections by a given variable pairing
        df_grouped = self.df.groupby([src_col, targ_col]).size().reset_index(name='count')

        # sort the df to only include rows with counts above a given number (aka min_connections)
        df_grouped = df_grouped[df_grouped['count'] >= min_connections]
        return df_grouped

