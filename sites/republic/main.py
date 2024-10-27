import os
from curl_cffi import requests
from pydantic import BaseModel, Field
from rich import print
from datetime import datetime, date
from src.models import Project

base_url = "https://europe.republic.com/"

# what we can read from api
class RepublicProject(BaseModel):
    name: str
    description: str | None
    currency: str
    cover_image: dict
    investment_raised: dict
    investment_sought: dict
    status: str
    allowed_to_invest: bool
    address: dict | None
    slug: str
    id: int
    listed: bool
    expires_at: datetime | None
    externally_approved_at: datetime | None

    def convert(self) -> Project:
        cc = "gb" if not self.address else self.address["country"].lower()
        return Project(
            name = self.name,
            name_short = self.name,
            external_link = base_url + self.slug,
            external_image_link = self.cover_image["cropped_location"],
            currency = self.currency,
            funding_current = self.investment_raised["amount_in_cents"], 
            funding_target = self.investment_sought["amount_in_cents"] if self.investment_sought["amount_in_cents"] else 0 ,
            funding_min = 0,
            funding_start = self.externally_approved_at if self.externally_approved_at else self.expires_at,
            funding_end=self.expires_at,
            description = self.description,
            description_short = self.description,
            location = cc,
        )

def main():
    session = requests.Session(impersonate="chrome")
    response = session.get("https://europe.republic.com/api/v1/campaigns?per_page=100&sort=trending_desc&allow_prereg_campaigns=true")
    response.raise_for_status() # TODO: error handling
    projects = []
    for p in response.json()["result"]:
        r_proj = RepublicProject(**p)
        if r_proj.listed:
            project = r_proj.convert()
            projects.append(project)
    return projects
    
if __name__ == "__main__":
    print(main())
