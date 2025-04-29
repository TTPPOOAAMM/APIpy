import aiohttp
import asyncio
from datetime import datetime

async def get_top_players(limit=50):
    API_URL = "https://osu.ppy.sh/api/v2"
    TOKEN_URL = "https://osu.ppy.sh/oauth/token"
    
    CLIENT_ID = "40346"
    CLIENT_SECRET = "Xoc2mJtfn6lLYC1PKxYfAbY4pCRLE1qEbLxcYeHT"
    
    async with aiohttp.ClientSession() as session:
        token_data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "public"
        }
        
        async with session.post(TOKEN_URL, data=token_data) as response:
            token_response = await response.json()
            access_token = token_response["access_token"]
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "mode": "osu",
            "limit": limit
        }
        
        async with session.get(f"{API_URL}/rankings/osu/performance", headers=headers, params=params) as response:
            players_data = await response.json()
        
        players = []
        for player in players_data["ranking"]:
            player_info = {
                "rank": player["global_rank"],
                "username": player["user"]["username"],
                "country": player["user"]["country_code"],
                "pp": round(player["pp"], 2),
                "accuracy": round(player["hit_accuracy"], 2),
                "play_count": player["play_count"],
                "play_time": player["play_time"] // 3600,  
                "total_score": player["total_score"],
                "ranked_score": player["ranked_score"],
                "level": player["level"]["current"],
            }
            players.append(player_info)
        
        return players

async def main():
    print(f"Загрузка топ 50 игроков osu!... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    try:
        top_players = await get_top_players()
        
        print("\nТоп 50 игроков osu! (режим osu!standard):")
        print("-" * 108)
        print(f"{'Ранг':<5} | {'Никнейм':<20} | {'Страна':<5} | {'PP':<8} | {'Точность':<8} | "
              f"{'Игр':<6} | {'Часов':<6} | {'Рейтинговые очки':<16} | {'Уровень':<7} | ")
        print("-" * 108)
        
        for player in top_players:
            print(f"{player['rank']:<5} | {player['username']:<20} | {player['country']:<5} | "
                  f"{player['pp']:<8} | {player['accuracy']:<8}% | "
                  f"{player['play_count']:<6} | {player["play_time"]:<6} | {player["ranked_score"]:<16} | {player['level']:<7} | ")
        
        total_pp = sum(p["pp"] for p in top_players)
        avg_pp = sum(p["pp"] for p in top_players) / len(top_players)
        avg_accuracy = sum(p["accuracy"] for p in top_players) / len(top_players)
        avg_play_count = sum(p["play_count"] for p in top_players) / len(top_players)
        avg_hour = sum(p["play_time"] for p in top_players) / len(top_players)
        
        print("\nОбщая статистика:")
        print(f"Суммарный PP топ 50: {round(total_pp, 2)}")
        print(f"Среднее PP: {round(avg_pp, 2)}")
        print(f"Средняя точность: {round(avg_accuracy, 2)}%")
        print(f"Среднее количество игр: {round(avg_play_count, 2)}")
        print(f"Среднее количество часов: {round(avg_hour)}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())