import pack.modu as lib
import os


DATABASE_PATH = 'library.db'
USERS_FILE = 'users.csv'
BOOKS_FILE = 'books.json'


def main():
    # 步驟一：關於資料庫的建立
    if not os.path.exists(DATABASE_PATH):
        lib.create_database(DATABASE_PATH, USERS_FILE, BOOKS_FILE)

    # 步驟二：帳密登入作業
    while True:
        username = input("請輸入帳號：")
        password = input("請輸入密碼：")
        result = lib.login(DATABASE_PATH, username, password)
        if result:
            break

    # 顯示選單
    while True:
        print("-------------------")
        print("    資料表 CRUD")
        print("-------------------")
        print("    1. 增加記錄")
        print("    2. 刪除記錄")
        print("    3. 修改記錄")
        print("    4. 查詢記錄")
        print("    5. 資料清單")
        print("-------------------")
        choice = input("選擇要執行的功能(Enter離開)：")

        if choice == '1':
            add_book()
            print("")
        elif choice == '2':
            delete_book()
            print("")
        elif choice == '3':
            update_book()
            print("")
        elif choice == '4':
            search_books()
            print("")
        elif choice == '5':
            display_all_books()
            print("")
        elif choice == '':
            break
        else:
            print("=>無效的選擇")
            print("")
            continue


def add_book():
    title = input("請輸入要新增的標題：")
    author = input("請輸入要新增的作者：")
    publisher = input("請輸入要新增的出版社：")
    year = input("請輸入要新增的年份：")

    if not title or not author or not publisher or not year:
        print("=>給定的條件不足，無法進行新增作業")
        return

    lib.add_book(DATABASE_PATH, title, author, publisher, year)
    print("異動 1 記錄")
    display_all_books()


def delete_book():
    display_all_books()
    title = input("請問要刪除哪一本書？：")

    if not title:
        print("=>給定的條件不足，無法進行刪除作業")
        return

    lib.delete_book(DATABASE_PATH, title)
    print("異動 1 記錄")
    display_all_books()


def update_book():
    display_all_books()
    title = input("請問要修改哪一本書的標題？：")
    new_title = input("請輸入要更改的標題：")
    author = input("請輸入要更改的作者：")
    publisher = input("請輸入要更改的出版社：")
    year = input("請輸入要更改的年份：")
    if not title or not new_title or not author or not publisher or not year:
        print("=>給定的條件不足，無法進行修改作業")
        return
    lib.update_book(DATABASE_PATH, title, new_title, author, publisher, year)
    print("異動 1 記錄")
    display_all_books()


def search_books():
    keyword = input("請輸入想查詢的關鍵字：")
    goal = lib.search_books(DATABASE_PATH, keyword)
    # print(type(goal))    # test code
    # print(goal)  # test code
    if not goal:
        print("找不到符合條件的書籍。")
    else:
        display_books(goal)


def display_all_books():
    books = lib.get_all_books(DATABASE_PATH)
    # print(type(books))  # test code
    # print(books)    # test code
    display_books(books)


def display_books(books):
    if books:
        print("|  title  |   author   |  publisher  |   year  |")
        for book in books:
            print(f"|{book[1]:<9}|{book[2]:<11}|{book[3]:<13}|{book[4]:<8}|")
    else:
        print("資料庫中無書籍。")


if __name__ == "__main__":
    main()
