import os
from curl_cffi import requests
from pydantic import BaseModel, Field
from rich import print

from src.models import Project

# what we can read from api
class EconeersProject(BaseModel):
    name: str
    link: str
    imgSrc: str
    sum: int
    threshold: int
    goal: int
    status: str
    fundingStarts: str
    fundingWillEnd: str
    
    def convert(self) -> Project:
        return Project(
            name = self.name,
            name_short = self.name,
            external_link = self.link,
            external_image_link = self.imgSrc,
            currency = "EUR",
            funding_current = self.sum, 
            funding_min = self.threshold,
            funding_target = self.goal,
            funding_start=self.fundingStarts,
            funding_end=self.fundingWillEnd,
            description = "",
            description_short = "",
            location = "de",
        )

def main():
    session = requests.Session(impersonate="chrome")
    response = session.get("https://www.econeers.de/api/v1/fundings")
    response.raise_for_status() # TODO: error handling
    projects = []
    for p in response.json():
        e_proj = EconeersProject(**p)
        if e_proj.link == "" or e_proj.sum == 0:
            continue
        if e_proj.status == "preview" or e_proj.status == "current":
            projects.append(e_proj.convert())
    return projects
    
if __name__ == "__main__":
    print(main())
