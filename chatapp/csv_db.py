import csv
from agno.tools import tool


# 定数としてファイル名を定義
FILENAME = "data.csv"


@tool(description="指定された名前と年齢をCSVファイルに登録します。")
def register_to_csv(name: str, age: int):
    try:
        with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, age])
        return {"status": "success", "message": f"{name}（{age}歳）を登録しました。"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool(description="CSVファイルから指定された名前のユーザー情報を検索します。")
def search_in_csv(search_name: str):
    results = []
    try:
        with open(FILENAME, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == search_name:
                    results.append({"name": row[0], "age": row[1]})
        if results:
            return {"status": "found", "results": results}
        else:
            return {
                "status": "not_found",
                "message": f"{search_name} は見つかりませんでした。",
            }
    except FileNotFoundError:
        return {"status": "error", "message": "CSVファイルが存在しません。"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
