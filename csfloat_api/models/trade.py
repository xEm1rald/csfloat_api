class Statistics:
    def __init__(self, median_trade_time=0, total_avoided_trades=0, total_failed_trades=0, total_trades=0, total_verified_trades=0):
        self.median_trade_time = median_trade_time
        self.total_avoided_trades = total_avoided_trades
        self.total_failed_trades = total_failed_trades
        self.total_trades = total_trades
        self.total_verified_trades = total_verified_trades

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            median_trade_time=data.get("median_trade_time", 0),
            total_avoided_trades=data.get("total_avoided_trades", 0),
            total_failed_trades=data.get("total_failed_trades", 0),
            total_trades=data.get("total_trades", 0),
            total_verified_trades=data.get("total_verified_trades", 0)
        )

class User:
    def __init__(self, steam_id=None, username=None, avatar=None, away=False, flags=0, online=False, stall_public=False, statistics=None):
        self.steam_id = steam_id
        self.username = username
        self.avatar = avatar
        self.away = away
        self.flags = flags
        self.online = online
        self.stall_public = stall_public
        self.statistics = Statistics.from_dict(statistics) if isinstance(statistics, dict) else statistics

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            steam_id=data.get("steam_id"),
            username=data.get("username"),
            avatar=data.get("avatar"),
            away=data.get("away", False),
            flags=data.get("flags", 0),
            online=data.get("online", False),
            stall_public=data.get("stall_public", False),
            statistics=data.get("statistics")
        )

class Item:
    def __init__(self, asset_id=None, def_index=None, sticker_index=None, icon_url=None, rarity=None, market_hash_name=None, tradable=0, inspect_link=None, is_commodity=False, type=None, rarity_name=None, type_name=None, item_name=None, serialized_inspect=None, gs_sig=None):
        self.asset_id = asset_id
        self.def_index = def_index
        self.sticker_index = sticker_index
        self.icon_url = icon_url
        self.rarity = rarity
        self.market_hash_name = market_hash_name
        self.tradable = tradable
        self.inspect_link = inspect_link
        self.is_commodity = is_commodity
        self.type = type
        self.rarity_name = rarity_name
        self.type_name = type_name
        self.item_name = item_name
        self.serialized_inspect = serialized_inspect
        self.gs_sig = gs_sig

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            asset_id=data.get("asset_id"),
            def_index=data.get("def_index"),
            sticker_index=data.get("sticker_index"),
            icon_url=data.get("icon_url"),
            rarity=data.get("rarity"),
            market_hash_name=data.get("market_hash_name"),
            tradable=data.get("tradable", 0),
            inspect_link=data.get("inspect_link"),
            is_commodity=data.get("is_commodity", False),
            type=data.get("type"),
            rarity_name=data.get("rarity_name"),
            type_name=data.get("type_name"),
            item_name=data.get("item_name"),
            serialized_inspect=data.get("serialized_inspect"),
            gs_sig=data.get("gs_sig")
        )

class SteamOffer:
    def __init__(self, id=None, state=None, is_from_seller=False, can_cancel_at=None, sent_at=None, deadline_at=None, updated_at=None):
        self.id = id
        self.state = state
        self.is_from_seller = is_from_seller
        self.can_cancel_at = can_cancel_at
        self.sent_at = sent_at
        self.deadline_at = deadline_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        # Explicit mapping ensures no positional argument errors
        return cls(
            id=data.get("id"),
            state=data.get("state"),
            is_from_seller=data.get("is_from_seller", False),
            can_cancel_at=data.get("can_cancel_at"),
            sent_at=data.get("sent_at"),
            deadline_at=data.get("deadline_at"),
            updated_at=data.get("updated_at")
        )

class Contract:
    def __init__(self, id=None, created_at=None, type=None, price=0, state=None, seller=None, reference=None, item=None, is_seller=False, is_watchlisted=False, watchers=0, sold_at=None):
        self.id = id
        self.created_at = created_at
        self.type = type
        self.price = price
        self.state = state
        self.seller = User.from_dict(seller)
        self.item = Item.from_dict(item)
        self.is_seller = is_seller
        self.is_watchlisted = is_watchlisted
        self.watchers = watchers
        self.sold_at = sold_at

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            id=data.get("id"),
            created_at=data.get("created_at"),
            type=data.get("type"),
            price=data.get("price", 0),
            state=data.get("state"),
            seller=data.get("seller"),
            item=data.get("item"),
            is_seller=data.get("is_seller", False),
            is_watchlisted=data.get("is_watchlisted", False),
            watchers=data.get("watchers", 0),
            sold_at=data.get("sold_at")
        )

class Trade:
    def __init__(self, id=None, created_at=None, buyer_id=None, buyer=None, seller_id=None, seller=None, contract_id=None, accepted_at=None, state=None, verification_mode=None, steam_offer=None, verify_sale_at=None, inventory_check_status=None, trade_protection_ends_at=None, contract=None, trade_url=None, trade_token=None, wait_for_cancel_ping=False, is_settlement_period=False):
        self.id = id
        self.created_at = created_at
        self.buyer_id = buyer_id
        self.buyer = User.from_dict(buyer)
        self.seller_id = seller_id
        self.seller = User.from_dict(seller)
        self.contract_id = contract_id
        self.accepted_at = accepted_at
        self.state = state
        self.verification_mode = verification_mode
        self.steam_offer = SteamOffer.from_dict(steam_offer)
        self.verify_sale_at = verify_sale_at
        self.inventory_check_status = inventory_check_status
        self.trade_protection_ends_at = trade_protection_ends_at
        self.contract = Contract.from_dict(contract)
        self.trade_url = trade_url
        self.trade_token = trade_token
        self.wait_for_cancel_ping = wait_for_cancel_ping
        self.is_settlement_period = is_settlement_period

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            id=data.get("id"),
            created_at=data.get("created_at"),
            buyer_id=data.get("buyer_id"),
            buyer=data.get("buyer"),
            seller_id=data.get("seller_id"),
            seller=data.get("seller"),
            contract_id=data.get("contract_id"),
            accepted_at=data.get("accepted_at"),
            state=data.get("state"),
            verification_mode=data.get("verification_mode"),
            steam_offer=data.get("steam_offer"),
            verify_sale_at=data.get("verify_sale_at"),
            inventory_check_status=data.get("inventory_check_status"),
            trade_protection_ends_at=data.get("trade_protection_ends_at"),
            contract=data.get("contract"),
            trade_url=data.get("trade_url"),
            trade_token=data.get("trade_token"),
            wait_for_cancel_ping=data.get("wait_for_cancel_ping", False),
            is_settlement_period=data.get("is_settlement_period", False)
        )