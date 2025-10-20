import pandas as pd
import numpy as np


class Structural_Diversity:
    # Possible column names for diameter at breast height
    DBH_COLUMN_NAMES = [
        'dbh', 'DBH', 'diameter', 'Diameter',
        'diameter_breast_height', 'diameter_at_breast_height',
        'tree_diameter', 'stem_diameter', 'diam'
    ]

    def __init__(self, data):
        self.data = data
        self.dbh_column = None
        self._find_dbh_column()

    def _find_dbh_column(self):
        """Find which DBH column exists in the dataset"""
        for col_name in self.DBH_COLUMN_NAMES:
            if col_name in self.data.columns:
                self.dbh_column = col_name
                print(f"Found DBH column: {col_name}")
                return

        raise ValueError(f"No DBH column found. Looking for one of: {self.DBH_COLUMN_NAMES}")

    def calculate_basal_area(self):
        """
        Calculate basal area for each tree
        Formula: BA = π * (DBH/2)² = π * r²
        Assumes DBH is in cm, returns BA in cm²
        """
        if self.dbh_column is None:
            raise ValueError("DBH column not found")

        # Calculate basal area: π * (diameter/2)²
        self.data['basal_area'] = np.pi * (self.data[self.dbh_column] / 2) ** 2

        return self.data

# Example usage:
# df = pd.DataFrame({'dbh': [20, 30, 25, 40]})
# sd = Structural_Diversity(df)
# df_with_ba = sd.calculate_basal_area()