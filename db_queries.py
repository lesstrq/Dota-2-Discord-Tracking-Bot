from db_connection import connect


def get_dota_id(discord_id):
    connection = connect()
    cursor = connection.cursor()
    query = f"SELECT dota_id FROM dota_track.discord_to_steam WHERE discord_id='{discord_id}'"
    cursor.execute(query)
    dota_id = cursor.fetchone()
    connection.close()
    if dota_id:
        return dota_id[0]
    return None


def insert_dota_id(discord_id, dota_id):
    connection = connect()
    cursor = connection.cursor()
    query = f"INSERT INTO dota_track.discord_to_steam VALUES ({discord_id}, {dota_id})"
    cursor.execute(query)
    connection.commit()
    connection.close()


def delete_record(discord_id):
    connection = connect()
    cursor = connection.cursor()
    delete_query = f"delete from dota_track.discord_to_steam where discord_id='{discord_id}'"
    cursor.execute(delete_query)
    connection.commit()
    connection.close()
