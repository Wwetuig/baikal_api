from typing import Optional

from pydantic import BaseModel

class FirstSputnikDataCreate(BaseModel):
    link: str
    description: Optional[str] = None
    measured_parameters_id: int
    measuring_devices_id: int
    month_id: int
    years_id: int
    day_id: int
    file_number: int
    times_day_id: int
    data_type_id: int

class FirstSputnikDataResponse(FirstSputnikDataCreate):
    id: int

    class Config:
        from_attributes = True


class SecondSputnikDataCreate(BaseModel):
    link: str
    description: Optional[str] = None
    measured_parameters_id: int
    measuring_devices_id: int
    month_id: int
    file_number: int
    times_day_id: int
    data_type_id: int

class SecondSputnikDataResponse(SecondSputnikDataCreate):
    id: int

    class Config:
        from_attributes = True


class ThirdSputnikDataCreate(BaseModel):
    link: str
    description: Optional[str] = None
    measured_parameters_id: int
    measuring_devices_id: int
    month_id: int
    file_number: int
    times_day_id: int
    data_type_id: int
    #splitting date_range to start_date and end_date
    #start_date: date
    #end_date: date

class ThirdSputnikDataResponse(ThirdSputnikDataCreate):
    id: int

    class Config:
        from_attributes = True