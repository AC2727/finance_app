from database import get_connection, init_db

init_db()


def add_transaction(amount, category, tx_type, description=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (amount, category, type, description)
        VALUES (?, ?, ?, ?)
        """,
        (amount, category, tx_type, description)
    )

    conn.commit()
    conn.close()


def get_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount, category, type, description, created_at
        FROM transactions
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
        FROM transactions
    """)

    income, expense = cursor.fetchone()
    conn.close()

    return income or 0, expense or 0

def get_monthly_report(year, month):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            type,
            SUM(amount) as total
        FROM transactions
        WHERE strftime('%Y', created_at) = ?
          AND strftime('%m', created_at) = ?
        GROUP BY type
        """,
        (str(year), f"{month:02d}")
    )

    rows = cursor.fetchall()
    conn.close()

    report = {"income": 0, "expense": 0}
    for tx_type, total in rows:
        report[tx_type] = total

    return report

