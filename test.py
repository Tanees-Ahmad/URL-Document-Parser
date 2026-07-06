import requests
from bs4 import BeautifulSoup


def print_secret_message(doc_url: str) -> None:

    grid, max_x, max_y = _fetch_and_parse_grid(doc_url)
    _print_grid(grid, max_x, max_y)


def _fetch_and_parse_grid(doc_url: str):

    response = requests.get(doc_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("No table found in the document.")

    grid = {}
    max_x = 0
    max_y = 0

    rows = table.find_all("tr")
    for row in rows[1:]:  # first row is the header: skip it
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        x_text = cells[0].get_text(strip=True)
        char_text = cells[1].get_text()
        y_text = cells[2].get_text(strip=True)

        if not x_text or not y_text:
            continue

        try:
            x = int(x_text)
            y = int(y_text)
        except ValueError:
            continue

        char = char_text if char_text else " "
        grid[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    return grid, max_x, max_y


def _print_grid(grid: dict, max_x: int, max_y: int) -> None:
    if not grid:
        print("")
        return

    lines = []
    for y in range(max_y, -1, -1):
        row_chars = [grid.get((x, y), " ") for x in range(max_x + 1)]
        lines.append("".join(row_chars))

    print("\n".join(lines))


if __name__ == "__main__":
    example_url = (
        "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
    )
    print_secret_message(example_url)