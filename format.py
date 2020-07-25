import pandas as pd
import os

columns = ("province", "lv_of_gov", "organization", "riding_name", "about_district",\
    "about_council", "election_info", "primary_role", "other_role", "bio", "name", "first_name", "last_name",\
    "gender", "party_name", "email", "photo_url", "source_url", "website", "facebook", "instagram", "twitter", "linkedin",\
    "youtube", "office_type", "address", "phone", "fax")

class Row:
    """
    An instance of this class represents a row in the exported CSV
    """

    def __init__(self, province, lv_of_gov, organization, riding_name, about_district,\
        about_council, election_info, primary_role, other_role, bio, name, first_name, last_name,\
        gender, party_name, email, photo_url, source_url, website, facebook, instagram, twitter, linkedin,\
        youtube, office_type, address, phone, fax):
        self.data = [province, lv_of_gov, organization, riding_name, about_district,\
            about_council, election_info, primary_role, other_role, bio, name, first_name, last_name,\
            gender, party_name, email, photo_url, source_url, website, facebook, instagram, twitter, linkedin,\
            youtube, office_type, address, phone, fax]

class Data:
    """
    The dataframe variable holds the data to be exported later, you can also use
    the append function to add a new row to the bottom of the dataframe.
    You can finally use the export function to export the dataframe as csv
    """

    dataframe = pd.DataFrame(columns=columns)

    def append(self, row: Row) -> None:
        self.dataframe.loc[self.dataframe.shape[0]] = row.data

    def export(self, filename: str) -> None:
        if not os.path.exists("./csv"):
            os.mkdir("csv")
        self.dataframe.to_csv("./csv"+filename)
         
