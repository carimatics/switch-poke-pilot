import annotated_types
from pydantic import PositiveFloat, BaseModel, model_validator
from typing_extensions import Annotated

Ratio = Annotated[PositiveFloat, annotated_types.Le(1.0)]


class ImageRegion(BaseModel):
    x: tuple[Ratio, Ratio]
    y: tuple[Ratio, Ratio]

    @model_validator(mode="after")
    def check_range(self) -> 'ImageRegion':
        if self.x[0] >= self.x[1]:
            raise ValueError(f"x[0] < x[1] required: {self.x[0]} >= {self.x[1]}")
        if self.y[0] >= self.y[1]:
            raise ValueError(f"y[0] < y[1] required: {self.y[0]} >= {self.y[1]}")
        return self
