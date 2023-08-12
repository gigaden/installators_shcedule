from db.crud import take_all_routs_for_day, add_distance_and_routes
from utils.find_distance import find_distance


# функция расчитывает расстояние за день, и заносит в бд вместе с адресами
async def finish_day(tg_id: int, year: int, month: int, day: int):
    all_coordinates, all_full_addresses = await take_all_routs_for_day(tg_id, year, month, day)
    day_distance: float = find_distance(all_coordinates)
    await add_distance_and_routes(tg_id, year, month, day, all_full_addresses, day_distance)
