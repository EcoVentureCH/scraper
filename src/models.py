from pydantic import BaseModel, Field
from datetime import datetime

# what we want in the end
class Project(BaseModel):
    name: str
    name_short: str
    external_link: str = Field(..., min_length=1) # TODO: use Url() for all links
    external_image_link: str
    currency: str # TODO: use something more specific for currency maybe?
    funding_current: int # in cents of that currency
    funding_min: int
    funding_target: int
    funding_start: datetime
    funding_end: datetime
    description: str | None
    description_short: str | None
    location: str
    
