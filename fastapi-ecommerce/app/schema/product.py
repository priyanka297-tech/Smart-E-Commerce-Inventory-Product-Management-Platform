from pydantic import (BaseModel, 
                      Field, 
                      AnyUrl, 
                      field_validator,
                      model_validator,
                      computed_field,
                      EmailStr)

from typing import Annotated, Literal, Optional
from uuid import UUID
from datetime import datetime

class Seller(BaseModel):
    seller_id: UUID
    name: Annotated[str, 
    Field(
        min_length=1,
        max_length=100,
        title="Seller Name",
        description="Name of the seller",
        example=["Seller A", "Seller B"],

    ),
    ]
    email: EmailStr
    website: AnyUrl
    
    @field_validator("email", mode="after")
    @classmethod
    def validate_email_domain(cls, value: EmailStr):
        allowed_domains = ["example.com", "test.com","test.in","mistore.in",
                           "realmeoofficial.com","samsung.com","apple.com",
                           "lenovo.com","dell.com","hp.com","asus.com",
                           "sony.com","oneplus.com","nokia.com","motorola.com","lg.com"
                           ]
        
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"seller domain not allowed")
        return value


class DimensionsCM(BaseModel):
    length: Annotated[float, Field(ge=0, description="Length in centimeters", example=10.0)]
    width: Annotated[float, Field(ge=0, description="Width in centimeters", example=5.0)]
    height: Annotated[float, Field(ge=0, description="Height in centimeters", example=2.0)]
    

class Product(BaseModel):
    id: UUID 
    
    sku: Annotated[
        str, 
        Field(
        min_length=1, 
        max_length=50, 
        title="SKU",
        description="Stock Keeping Unit (SKU) of the product",
        example=["SKU12345", "SKU67890"], ),
    ]
    
    name: Annotated[str, Field(
        min_length=1,
        max_length=100,
        title="Name",
        description="Name of the product",
        example=["Product A", "Product B"]
    )]
    
    category: Annotated[str, Field(
        min_length=1,
        max_length=50,
        title="Category",
        description="Category of the product",
        example=["Electronics", "Clothing"]
    )]
    
    description: Annotated[str, Field(
        min_length=1,
        max_length=200,
        title="Description",
        description="Description of the product",
        example=["Description A", "Description B"]
    )]
    
    price: Annotated[float, Field(
        ge=0,
        title="Price",
        description="Price of the product",
        example=[19.99, 29.99]
    )]
    
    brand: Annotated[str, Field(
        min_length=1,
        max_length=50,
        title="Brand",
        description="Brand of the product",
        example=["Brand A", "Brand B"]
    )]
    currency: Literal["INR"] = "INR" 
    
    discount_percent: Annotated[float, Field(
        ge=0, le=90,
        title="Discount Percent",
        description="Discount percentage of the product",
        example=[10.0, 20.0]
    )]
    
    stock: Annotated[int, Field(
        ge=0,
        title="Stock",
        description="Stock quantity of the product",
        example=[10, 20]
    )]
    
    is_active: Annotated[bool, Field(
        title="Is Active",
        description="Indicates if the product is active",
        example=[True, False]
    )]
    
    rating: Annotated[float, Field(
        ge=0, le=5,
        title="Rating",
        description="Rating of the product",
        example=[4.0, 4.5]
    )]
    
    tags: Annotated[Optional[list[str]], Field(
        default=None,
        title="Tags",
        description="Upto 10 tags for the product",
        example=[["tag1", "tag2"], ["tag3", "tag4"]]
    )]
    
    image_urls: Optional[list[AnyUrl]] = None
    
    dimensions_cm: DimensionsCM
    seller: Seller
    created_at: datetime
    
    
    
    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value: str):
        if "-" not in value :
            raise ValueError("SKU must have "-" as separator")
        
        last = value.split("-")[-1]
        if not len(last) == 3 and last.isdigit():
            raise ValueError("SKU must end with 3 numeric characters")
        return value
    
    
    @model_validator(mode="after")
    @classmethod
    def validate_bussiness_rules(cls,model:"Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("if stock is zero, is_active must be false")
        
        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted products must have the rating")
        return model
    
    
    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1-self.discount_percent/100), 2)
    
    
    @computed_field
    @property
    def volume_cm3(self) -> float:
        d = self.dimensions_cm
        return round(d.length * d.width * d.height, 2)
    
class ProductUpdate(BaseModel):
    name: Optional[Annotated[str, Field(
        min_length=1,
        max_length=100,
        title="Name",
        description="Name of the product",
        example=["Product A", "Product B"]
    )]]
    
    category: Optional[Annotated[str, Field(
        min_length=1,
        max_length=50,
        title="Category",
        description="Category of the product",
        example=["Electronics", "Clothing"]
    )]]
    
    description: Optional[Annotated[str, Field(
        min_length=1,
        max_length=200,
        title="Description",
        description="Description of the product",
        example=["Description A", "Description B"]
    )]]
    
    price: Optional[Annotated[float, Field(
        ge=0,
        title="Price",
        description="Price of the product",
        example=[19.99, 29.99]
    )]]
    
    brand: Optional[Annotated[str, Field(
        min_length=1,
        max_length=50,
        title="Brand",
        description="Brand of the product",
        example=["Brand A", "Brand B"]
    )]]
    
    discount_percent: Optional[Annotated[float, Field(
        ge=0, le=90,
        title="Discount Percent",
        description="Discount percentage of the product",
        example=[10.0, 20.0]
    )]]
    
    stock: Optional[Annotated[int, Field(
        ge=0,
        title="Stock",
        description="Stock quantity of the product",
        example=[10, 20]
    )]]
    
    is_active: Optional[Annotated[bool, Field(
        title="Is Active",
        description="Indicates if the product is active",
        example=[True, False]
    )]]
    
    rating: Optional[Annotated[float, Field(
        ge=0, le=5,
        title="Rating",
        description="Rating of the product",
        example=[4.0, 4.5]
    )]]
    
class SellerUpdate(BaseModel):
    name: Optional[Annotated[str, Field(
        min_length=1,
        max_length=100,
        title="Seller Name",
        description="Name of the seller",
        example=["Seller A", "Seller B"],

    )]]

        
class DimensionsUpdate(BaseModel):
    length: Optional[Annotated[float, Field(ge=0, description="Length in centimeters", example=10.0)]]
    width: Optional[Annotated[float, Field(ge=0, description="Width in centimeters", example=5.0)]]
    height: Optional[Annotated[float, Field(ge=0, description="Height in centimeters", example=2.0)]]
    
    
class ProductUpdateRequest(BaseModel):
    name: Optional[Annotated[str, Field(
        min_length=1,
        max_length=100,
        title="Name",
        description="Name of the product",
        example=["Product A", "Product B"]
    )]]
    
    category: Optional[Annotated[str, Field(
        min_length=1,
        max_length=50,
        title="Category",
        description="Category of the product",
        example=["Electronics", "Clothing"]
    )]]
    
    description: Optional[Annotated[str, Field(
        min_length=1,
        max_length=200,
        title="Description",
        description="Description of the product",
        example=["Description A", "Description B"]
    )]]
    
    price: Optional[Annotated[float, Field(
        ge=0,
        title="Price",
        description="Price of the product",
        example=[19.99, 29.99]
    )]]
    
    brand: Optional[Annotated[str, Field(
        min_length=1,
        max_length=50,
        title="Brand",
        description="Brand of the product",
        example=["Brand A", "Brand B"]
    )]]
    
    discount_percent: Optional[Annotated[float, Field(
        ge=0, le=90,
        title="Discount Percent",
        description="Discount percentage of the product",
        example=[10.0, 20.0]
    )]]
    
    stock: Optional[Annotated[int, Field(
        ge=0,
        title="Stock",
        description="Stock quantity of the product",
        example=[10, 20]
    )]]
    
    is_active: Optional[Annotated[bool, Field(
        title="Is Active",
        description="Indicates if the product is active",
        example=[True, False]
    )]]
    
    rating: Optional[Annotated[float, Field(
        ge=0, le=5,
        title="Rating",
        description="Rating of the product",
        example=[4.0, 4.5]
    )]]
    
    class SellerUpdate(BaseModel):
        name: Optional[Annotated[str, Field(
            min_length=1,
            max_length=100,
            title="Seller Name",
            description="Name of the seller",
            example=["Seller A", "Seller B"],

        )]]
        
        


    