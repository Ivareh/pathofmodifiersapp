from typing import Callable, Dict, List, Tuple
import pytest

import app.tests.api.api_routes_test_base as test_api
from app.tests.utils.model_utils.account import (
    create_random_account_dict,
    generate_random_account,
)
from app.crud.base import ModelType
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.core.models.models import Account
from app.api.api_v1.endpoints import account_prefix
from app.tests.utils.utils import get_model_table_name, get_model_unique_identifier


@pytest.fixture(scope="module")
def model_name() -> str:
    table_name = get_model_table_name(Account)
    return table_name


@pytest.fixture(scope="module")
def route_name() -> str:
    return account_prefix


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    unique_identifier = get_model_unique_identifier(Account)
    return unique_identifier


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    """Some models require high permissions to test GET requests

    Returns:
        bool: True if the model requires high permissions to test GET requests
    """
    return True


@pytest.fixture(scope="module")
def update_request_params() -> bool:
    """Some models require params to PUT request in the url

    Returns:
        bool: True if the model requires params in the PUT request
    """
    return False


@pytest.fixture(scope="module")
def ignore_test_columns() -> List[str]:
    """Ignore these columns when testing the model

    updatedAt and createdAt are ignored because currently, the API returns
    time in a different format than the one stored in the database

    Returns:
        List[str]: List of columns to ignore
    """
    return ["updatedAt", "createdAt"]


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Tuple[Dict, ModelType]]:
    return generate_random_account


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], Dict]:
    return create_random_account_dict


class TestAccount(test_api.TestAPI):
    pass
