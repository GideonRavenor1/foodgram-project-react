from typing import TypedDict


class IngredientResult(TypedDict, total=False):
    name: str
    amount: int
    measurement_unit: str


class RecipeResult(TypedDict, total=False):
    name: str
    text: str
    image: str
    cooking_time: int
    tag: str
    ingredients: list[IngredientResult]
