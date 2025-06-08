from enum import Enum


class Permissions(Enum):
    VIEW_PRODUCT = "view_product"
    UPDATE_PRODUCT = "update_product"
    ADD_PRODUCT = "add_product"
    DELETE_PRODUCT = "delete_product"

    @classmethod
    def list(cls):
        return [permission.value for permission in cls]