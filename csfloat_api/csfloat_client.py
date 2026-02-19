import aiohttp
import re
from aiohttp_socks.connector import ProxyConnector
from aiohttp.resolver import ThreadedResolver
from typing import Iterable, Union, Optional, Dict, List, Any, Literal

# Import the Pydantic models
from .models.listing import Listing
from .models.buy_orders import BuyOrders
from .models.me import Me
from .models.stall import Stall
from .models.trade import Trade

__all__ = ("Client",)

_API_URL = 'https://csfloat.com/api/v1'


class Client:
    _SUPPORTED_METHODS = ('GET', 'POST', 'DELETE', 'PATCH')
    ERROR_MESSAGES = {
        401: 'Unauthorized -- Your API key is wrong.',
        403: 'Forbidden -- The requested resource is hidden for administrators only.',
        404: 'Not Found -- The specified resource could not be found.',
        405: 'Method Not Allowed -- You tried to access a resource with an invalid method.',
        406: 'Not Acceptable -- You requested a format that isn\'t json.',
        410: 'Gone -- The requested resource has been removed from our servers.',
        418: 'I\'m a teapot.',
        429: 'Too Many Requests -- You\'re requesting too many resources! Slow down!',
        500: 'Internal Server Error -- We had a problem with our server. Try again later.',
        503: 'Service Unavailable -- We\'re temporarily offline for maintenance. Please try again later.',
    }

    __slots__ = (
        "API_KEY",
        "proxy",
        "_headers",
        "_connector",
        "_session"
    )

    def __init__(self, api_key: str, proxy: Optional[str] = None) -> None:
        self.API_KEY = api_key
        self.proxy = proxy
        self._validate_proxy()
        self._headers = {
            'Authorization': self.API_KEY
        }

        safe_resolver = ThreadedResolver()

        if self.proxy:
            self._connector = ProxyConnector.from_url(
                self.proxy,
                ttl_dns_cache=300,
                resolver=safe_resolver
            )
        else:
            self._connector = aiohttp.TCPConnector(
                resolver=safe_resolver,
                limit_per_host=50
            )

        self._session = aiohttp.ClientSession(connector=self._connector, headers=self._headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._session.close()

    async def close(self):
        await self._session.close()

    def _validate_proxy(self) -> None:
        """Validates the proxy URL format."""
        if not self.proxy:
            return
        pattern = r'^(socks5|socks4|http|https)://(\w+:\w+@)?[\w.-]+:\d+$'
        if not re.match(pattern, self.proxy):
            raise ValueError(
                f"Invalid proxy URL format: {self.proxy}. Expected format like 'socks5://user:pass@host:port'")
        port = self.proxy.split(':')[-1]
        if not port.isdigit() or not (1 <= int(port) <= 65535):
            raise ValueError(f"Invalid port in proxy URL: {port}")

    async def _request(self, method: str, parameters: str, json_data: Any = None) -> Optional[dict]:
        if method not in self._SUPPORTED_METHODS:
            raise ValueError('Unsupported HTTP method.')

        url = f'{_API_URL}{parameters}'

        async with self._session.request(method=method, url=url, ssl=False, json=json_data) as response:
            if response.status in self.ERROR_MESSAGES:
                raise Exception(self.ERROR_MESSAGES[response.status])

            if response.status != 200:
                try:
                    error_details = await response.json()
                except Exception:
                    error_details = await response.text()
                raise Exception(f'Error: {response.status}\nResponse Body: {error_details}')

            if response.content_type != 'application/json':
                raise Exception(f"Expected JSON, got {response.content_type}")

            return await response.json()

    def _validate_category(self, category: int) -> None:
        if category not in (0, 1, 2, 3):
            raise ValueError(f'Unknown category parameter "{category}"')

    def _validate_sort_by(self, sort_by: str) -> None:
        valid_sort_by = (
            'lowest_price', 'highest_price', 'most_recent', 'expires_soon',
            'lowest_float', 'highest_float', 'best_deal', 'highest_discount',
            'float_rank', 'num_bids'
        )
        if sort_by not in valid_sort_by:
            raise ValueError(f'Unknown sort_by parameter "{sort_by}"')

    def _validate_type(self, type_: str) -> None:
        if type_ not in ('buy_now', 'auction'):
            raise ValueError(f'Unknown type parameter "{type_}"')

    def _validate_role(self, role: str) -> None:
        valid_roles = ("seller", "buyer")
        if role not in valid_roles:
            raise ValueError(f'Unknown role parameter: {role}')

    async def get_exchange_rates(self) -> Optional[dict]:
        return await self._request(method="GET", parameters="/meta/exchange-rates")

    async def get_me(self, *, raw_response: bool = False) -> Union[Me, dict]:
        response = await self._request(method="GET", parameters="/me")
        if raw_response:
            return response
        return Me.model_validate(response)

    async def get_transactions(self, page: int = 0, limit: int = 10):
        return await self._request(method="GET", parameters=f"/me/transactions?page={page}&limit={limit}&order=desc")

    async def get_account_standing(self):
        return await self._request(method="GET", parameters="/me/account-standing")

    async def get_location(self) -> Optional[dict]:
        return await self._request(method="GET", parameters="/meta/location")

    async def get_pending_trades(self, limit: int = 500, page: int = 0) -> List[Trade]:
        parameters = f"/me/trades?state=pending&limit={limit}&page={page}"
        response = await self._request(method="GET", parameters=parameters)
        return [Trade.model_validate(raw_trade) for raw_trade in response.get("trades", [])]

    async def get_similar(self, *, listing_id: int, raw_response: bool = False) -> Union[List[Listing], dict]:
        parameters = f"/listings/{listing_id}/similar"
        response = await self._request(method="GET", parameters=parameters)
        if raw_response:
            return response
        return [Listing.model_validate(item) for item in response]

    async def get_buy_orders(self, *, listing_id: int, limit: int = 10, raw_response: bool = False) -> Union[
        List[BuyOrders], dict]:
        parameters = f"/listings/{listing_id}/buy-orders?limit={limit}"
        response = await self._request(method="GET", parameters=parameters)
        if raw_response:
            return response
        return [BuyOrders.model_validate(item) for item in response]

    async def get_my_buy_orders(self, *, page: int = 0, limit: int = 10):
        return await self._request(method="GET", parameters=f"/me/buy-orders?page={page}&limit={limit}&order=desc")

    async def get_sales(self, market_hash_name: str, paint_index: Optional[int] = None):
        parameters = f"/history/{market_hash_name}/sales"
        if paint_index is not None:
            parameters += f"?paint_index={paint_index}"
        return await self._request(method="GET", parameters=parameters)

    async def get_all_listings(
            self,
            *,
            min_price: Optional[int] = None,
            max_price: Optional[int] = None,
            cursor: Optional[str] = None,
            limit: int = 50,
            sort_by: str = 'best_deal',
            category: int = 0,
            def_index: Optional[Union[int, Iterable[int]]] = None,
            min_float: Optional[float] = None,
            max_float: Optional[float] = None,
            rarity: Optional[str] = None,
            paint_seed: Optional[int] = None,
            paint_index: Optional[int] = None,
            user_id: Optional[str] = None,
            collection: Optional[str] = None,
            market_hash_name: Optional[str] = None,
            type_: str = 'buy_now',
            raw_response: bool = False
    ) -> Union[Dict[str, Any], dict]:
        self._validate_category(category)
        self._validate_sort_by(sort_by)
        self._validate_type(type_)

        parameters = f'/listings?limit={limit}&sort_by={sort_by}&category={category}&type={type_}'
        if cursor: parameters += f'&cursor={cursor}'
        if min_price: parameters += f'&min_price={min_price}'
        if max_price: parameters += f'&max_price={max_price}'
        if def_index:
            if isinstance(def_index, Iterable) and not isinstance(def_index, str):
                def_index = ','.join(map(str, def_index))
            parameters += f'&def_index={def_index}'
        if min_float: parameters += f'&min_float={min_float}'
        if max_float: parameters += f'&max_float={max_float}'
        if rarity: parameters += f'&rarity={rarity}'
        if paint_seed: parameters += f'&paint_seed={paint_seed}'
        if paint_index: parameters += f'&paint_index={paint_index}'
        if user_id: parameters += f'&user_id={user_id}'
        if collection: parameters += f'&collection={collection}'
        if market_hash_name: parameters += f'&market_hash_name={market_hash_name}'

        response = await self._request(method='GET', parameters=parameters)

        if raw_response:
            return response

        listings = [Listing.model_validate(item) for item in response.get("data", [])]
        return {"listings": listings, "cursor": response.get("cursor")}

    async def get_specific_listing(self, listing_id: int, *, raw_response: bool = False) -> Union[Listing, dict]:
        parameters = f'/listings/{listing_id}'
        response = await self._request(method='GET', parameters=parameters)
        if raw_response:
            return response
        return Listing.model_validate(response)

    async def get_stall(self, user_id: int, *, limit: int = 40, raw_response: bool = False) -> Union[Stall, dict]:
        parameters = f'/users/{user_id}/stall?limit={limit}'
        response = await self._request(method='GET', parameters=parameters)
        if raw_response:
            return response
        return Stall.model_validate(response)

    async def get_inventory(self):
        return await self._request(method="GET", parameters="/me/inventory")

    async def get_watchlist(self, limit: int = 40):
        return await self._request(method="GET", parameters=f"/me/watchlist?limit={limit}")

    async def get_offers(self, limit: int = 40):
        return await self._request(method="GET", parameters=f"/me/offers-timeline?limit={limit}")

    async def get_trade_history(self, role: str = "seller", limit: int = 30, page: int = 0) -> List[Trade]:
        self._validate_role(role)
        parameters = f"/me/trades?role={role}&state=failed,cancelled,verified&limit={limit}&page={page}"
        response = await self._request(method="GET", parameters=parameters)
        return [Trade.model_validate(raw_trade) for raw_trade in response.get("trades", [])]

    async def get_trades(self, role: Literal["seller", "buyer"] = "seller", limit: int = 30, page: int = 0) -> List[
        Trade]:
        self._validate_role(role)
        parameters = f"/me/trades?role={role}&limit={limit}&page={page}"
        response = await self._request(method="GET", parameters=parameters)
        return [Trade.model_validate(raw_trade) for raw_trade in response.get("trades", [])]

    async def delete_listing(self, *, listing_id: int):
        return await self._request(method="DELETE", parameters=f"/listings/{listing_id}")

    async def delete_buy_order(self, *, id: int):
        return await self._request(method="DELETE", parameters=f"/buy-orders/{id}")

    async def delete_watchlist(self, *, id: int):
        return await self._request(method="DELETE", parameters=f"/listings/{id}/watchlist")

    async def create_listing(
            self,
            *,
            asset_id: str,
            price: float,
            type_: str = "buy_now",
            max_offer_discount: Optional[int] = None,
            reserve_price: Optional[float] = None,
            duration_days: Optional[int] = None,
            description: str = "",
            private: bool = False,
    ) -> Optional[dict]:
        self._validate_type(type_)
        json_data = {
            "asset_id": asset_id,
            "price": price,
            "type": type_,
            "description": description,
            "private": private
        }
        if max_offer_discount is not None: json_data["max_offer_discount"] = max_offer_discount
        if reserve_price is not None: json_data["reserve_price"] = reserve_price
        if duration_days is not None: json_data["duration_days"] = duration_days

        return await self._request(method="POST", parameters="/listings", json_data=json_data)

    async def create_buy_order(self, *, market_hash_name: str, max_price: int, quantity: int) -> Optional[dict]:
        json_data = {"market_hash_name": market_hash_name, "max_price": max_price, "quantity": quantity}
        return await self._request(method="POST", parameters="/buy-orders", json_data=json_data)

    async def make_offer(self, *, listing_id: int, price: int) -> Optional[dict]:
        json_data = {"contract_id": str(listing_id), "price": price, "cancel_previous_offer": False}
        return await self._request(method="POST", parameters="/offers", json_data=json_data)

    async def buy_now(self, *, total_price: int, listing_id: str) -> Optional[dict]:
        json_data = {"total_price": total_price, "contract_ids": [str(listing_id)]}
        return await self._request(method="POST", parameters="/listings/buy", json_data=json_data)

    async def accept_sale(self, *, trade_ids: List[str]):
        json_data = {"trade_ids": trade_ids}
        return await self._request(method="POST", parameters="/trades/bulk/accept", json_data=json_data)

    async def update_listing_price(self, *, listing_id: int, price: int):
        json_data = {"price": price}
        return await self._request(method="PATCH", parameters=f"/listings/{listing_id}", json_data=json_data)