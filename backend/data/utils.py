"""
utils.py

Printing utilities for analytics query results.

Usage:
    from utils import pprint_query, pprint_section

    pprint_section("Drive Scoring by Team", get_drive_scoring_by_team(conn))
    pprint_section("Drive Finishers",       get_drive_finishers(conn))
"""

def pprint_query(rows, title=None):
    """
    Prints a list of sqlite3.Row (or plain dicts) as a padded table.
    Handles empty result sets gracefully.
    """
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")

    if not rows:
        print("  (no results)\n")
        return

    # sqlite3.Row supports keys(); plain dicts use .keys() too
    columns = list(rows[0].keys())

    # Calculate column widths — max of header or any value
    widths = {
        col: max(len(col), max(len(str(row[col] or "")) for row in rows))
        for col in columns
    }

    # Header
    header = "  " + "  ".join(col.ljust(widths[col]) for col in columns)
    divider = "  " + "  ".join("-" * widths[col] for col in columns)
    print(header)
    print(divider)

    # Rows — right-align numbers, left-align strings
    for row in rows:
        parts = []
        for col in columns:
            val = row[col]
            width = widths[col]
            if isinstance(val, (int, float)) and val is not None:
                parts.append(str(val).rjust(width))
            else:
                parts.append(str(val or "").ljust(width))
        print("  " + "  ".join(parts))

    print(f"\n  {len(rows)} row(s)\n")


def pprint_section(title, rows):
    """Convenience wrapper — title + table in one call."""
    pprint_query(rows, title=title)


def pprint_all(conn, query_map):
    """
    Print multiple queries at once from a dict of
    { display_title: query_function }.

    Example:
        pprint_all(conn, {
            "Drive Scoring by Team":        get_drive_scoring_by_team,
            "Drive Finishers":              get_drive_finishers,
            "Defenders Beaten off Dribble": get_defenders_beaten_off_dribble,
        })
    """
    for title, fn in query_map.items():
        pprint_section(title, fn(conn))