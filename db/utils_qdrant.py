
def get_startdest(qdrant_client, anfrage):
    '''
    Get start and destination from a Qdrant client.
    anfrage type: 
        {
            "start": str|None,
            "start_bedingung": str|None,
            "ziel": str|None,
            "ziel_bedingung": str|None
        }

    return type:
    {
        "start": {
            "location": str,
            "neo4j_id": str,
            "name": str,
        } | None,
        "ziel": {
            "location": str,
            "neo4j_id": str,
            "name": str,
        } | None,
    }
    '''

