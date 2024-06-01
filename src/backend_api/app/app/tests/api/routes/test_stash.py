from typing import Awaitable, Callable, Dict, List, Tuple, Union
import pytest
from sqlalchemy.orm import Session

import app.tests.api.api_cascade_tests as test_cascade_api
from app.tests.utils.model_utils.stash import (
    create_random_stash_dict,
    generate_random_stash,
)
from app.crud.base import CRUDBase, ModelType
from app.tests.crud.crud_test_base import TestCRUD as UtilTestCRUD
from app.tests.crud.cascade_tests import TestCascade as UtilTestCascadeCRUD
from app.crud import CRUD_account
from app.core.models.models import Account, Stash


@pytest.fixture(scope="module")
def model_name() -> str:
    return Stash.__table__.name


@pytest.fixture(scope="module")
def route_name() -> str:
    return "stash"


@pytest.fixture(scope="module")
def unique_identifier() -> str:
    return "stashId"


@pytest.fixture(scope="module")
def get_crud_test_model() -> UtilTestCRUD:
    model = UtilTestCRUD()
    return model


@pytest.fixture(scope="module")
def get_crud_test_cascade_model() -> UtilTestCascadeCRUD:
    model = UtilTestCascadeCRUD()
    return model


@pytest.fixture(scope="module")
def get_high_permissions() -> bool:
    return False


@pytest.fixture(scope="module")
def object_create_func() -> Callable[[Session], Awaitable[Dict]]:
    async def create_object(db: Session) -> Dict:
        return await create_random_stash_dict(db)

    return create_object


@pytest.fixture(scope="module")
def object_generator_func() -> Callable[[], Tuple[Dict, ModelType]]:
    return generate_random_stash


@pytest.fixture(scope="module")
def create_random_object_func() -> Callable[[], Dict]:
    return create_random_stash_dict


@pytest.fixture(scope="module")
def object_generator_func_w_deps() -> (
    Callable[[], Tuple[Dict, Stash, List[Union[Dict, Account]]]]
):
    def generate_random_stash_w_deps(
        db,
    ) -> Callable[[], Tuple[Dict, Stash, List[Union[Dict, Account]]]]:
        return generate_random_stash(db, retrieve_dependencies=True)

    return generate_random_stash_w_deps


@pytest.fixture(scope="module")
def api_deps_instances() -> List[str]:
    """Fixture for API dependencies instances.

    Dependencies in return list needs to be in correct order.
    If a dependency is dependent on another, the dependency needs to occur later than
    the one its dependent on. The order is defined by 'generate_random_stash'.

    Returns:
        List[str]: API dependencies instances.


    """
    return [{"account": "accountName"}]


class TestStash(test_cascade_api.TestCascadeAPI):
    pass
