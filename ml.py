import scipy.sparse as sparse
import implicit
import os
import libsql_experimental as libsql
from dotenv import load_dotenv

load_dotenv()

TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# global model cache
model_cache = None

def get_db():
    # conn = libsql.connect("skill-swap", uri=TURSO_URL, auth_token=TURSO_TOKEN)
    conn = libsql.connect(
        TURSO_URL,
        auth_token=TURSO_TOKEN
    )

    return conn

async def get_all_interactions():
    db = get_db()
    query = """
        SELECT 
            user_id,
            skill_id,
            1 AS weight
        FROM Skill_Likes

        UNION ALL

        SELECT
            user_id,
            skill_id,
            2 AS weight
        FROM Comment

        UNION ALL

        SELECT
            uf.follower_id AS user_id,
            s.id AS skill_id,
            1.5 AS weight
        FROM user_follows AS uf
        JOIN Skill AS s ON s.user_id = uf.following_id
    """
    cursor = db.execute(query)
    rows = cursor.fetchall()
    # return [dict(row) for row in rows]
    return [
        {
            "user_id": row[0],
            "skill_id": row[1],
            "weight": row[2]
        }
        for row in rows
    ]

async def build_model():
    rows = await get_all_interactions()

    user_ids = list(set(r["user_id"] for r in rows))
    skill_ids = list(set(r["skill_id"] for r in rows))

    user_index = {uid: i for i, uid in enumerate(user_ids)}
    skill_index = {sid: i for i, sid in enumerate(skill_ids)}

    data, row_indices, col_indices = [], [], []
    for r in rows:
        row_indices.append(user_index[r["user_id"]])
        col_indices.append(skill_index[r["skill_id"]])
        data.append(r["weight"])

    matrix = sparse.csr_matrix(
        (data, (row_indices, col_indices)),
        shape=(len(user_ids), len(skill_ids))
    )

    model = implicit.als.AlternatingLeastSquares(factors=50, iterations=20)
    model.fit(matrix)

    return model, matrix, user_index, skill_index, skill_ids

async def load_model():
    global model_cache
    print("Training model...")
    model_cache = await build_model()
    print("Model ready!")

async def recommend(user_id, n=10):
    global model_cache

    if model_cache is None:
        await load_model()

    model, matrix, user_index, skill_index, skill_ids = model_cache

    if user_id not in user_index:
        print(f"User {user_id} has no interactions yet, returning trending skills")
        return await get_trending_skills(n)

    uid = user_index[user_id]
    recommended_ids, scores = model.recommend(uid, matrix[uid], N=n)

    results = [{"skill_id": skill_ids[i], "score": float(scores[j])}
               for j, i in enumerate(recommended_ids)]
    return results

async def get_trending_skills(n=10):
    db = get_db()
    cursor = db.execute("SELECT skill_id, COUNT(*) as total FROM Skill_Likes GROUP BY skill_id ORDER BY total DESC LIMIT ?", (n,))
    rows = cursor.fetchall()
    return [{"skill_id": row["skill_id"], "score": float(row["total"])} for row in rows]