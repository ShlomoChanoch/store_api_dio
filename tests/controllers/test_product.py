from typing import List
import time
from datetime import datetime, timezone
import pytest
from tests.factories import product_data
from fastapi import status
from store.core.exceptions import InsertionException


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()

    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8500",
        "status": True,
    }


async def test_controller_create_should_return_bad_request_when_insertion_error(
    client, products_url, monkeypatch
):
    def mock_create_exception(*args, **kwargs):
        raise InsertionException("Simulated insertion error")

    monkeypatch.setattr("store.usecases.product.ProductUsecase.create", mock_create_exception)

    response = await client.post(products_url, json=product_data())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Simulated insertion error"}


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8500",
        "status": True,
    }

async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1

async def test_controller_query_should_filter_by_price(client, products_url):
    await client.post(
        products_url, json=product_data(name="iPhone 15 Pro", price="7500")
    )
    await client.post(
        products_url, json=product_data(name="iPhone 13 Mini", price="4500")
    )
    await client.post(
        products_url, json=product_data(name="MacBook Pro", price="10500")
    )

    response = await client.get(f"{products_url}?min_price=5000&max_price=8000")

    assert response.status_code == status.HTTP_200_OK
    products = response.json()
    assert len(products) == 1
    assert products[0]["name"] == "iPhone 15 Pro"

async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7500"}
    )

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "7500",
        "status": True,
    }

async def test_controller_patch_should_automatically_update_updated_at(
    client, products_url, product_inserted
):
    original_updated_at = product_inserted.updated_at.replace(tzinfo=timezone.utc)
    time.sleep(0.001)

    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7500"}
    )

    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    new_updated_at = datetime.fromisoformat(content["updated_at"]).replace(
        tzinfo=timezone.utc
    )
    assert new_updated_at > original_updated_at

async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Produto não encontrado com o filtro: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }
