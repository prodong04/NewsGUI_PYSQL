import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import decimal
import dbModule
import tkinter.messagebox

db = dbModule.Database()


class KeywordService:
    def __init__(self, user_type):
        self.user_type = user_type
        self.db = db

    def authenticate(self):
        # 간단한 인증 메서드
        id_input = simpledialog.askstring("Authentication", "Enter ID:")
        pw_input = simpledialog.askstring("Authentication", "Enter Password:", show='*')

        if id_input == "admin" and pw_input == "1234":
            return "admin"
        elif id_input == "user" and pw_input == "1234":
            return "user"
        else:
            messagebox.showinfo("Authentication Failed", "Invalid ID or Password")
            return None

    def show_menu(self):
        root = tk.Tk()
        root.title("Keyword Service Menu")

        menu_label = ttk.Label(root, text="Select a Menu:")
        menu_label.pack(pady=10)

        menu_options = ["1. Daily Popular Keywords", "2. View Interesting News", "3. View Keyword Trend"
                        ]

        if self.user_type == "admin":
            menu_options = ["1. Manage Press", "2. Manage Articles", "3. Manage Reporters", "4. Show Monthly Article Number"]

        menu_listbox = tk.Listbox(root)
        for option in menu_options:
            menu_listbox.insert(tk.END, option)

        menu_listbox.pack(pady=10)

        select_button = ttk.Button(root, text="Select", command=lambda: self.execute_menu(menu_listbox.get(tk.ACTIVE)))
        select_button.pack(pady=10)

        root.mainloop()

    def execute_menu(self, selected_menu):
        if selected_menu.startswith("1."):
            # 일간 인기 키워드 또는 관리자 메뉴 중 언론사 관리
            if self.user_type == "admin":
                self.manage_press()
            else:
                self.daily_popular_keywords()
        elif selected_menu.startswith("2."):
            # 뉴스기사 확인 또는 기사 변경
            if self.user_type == "admin":
                self.manage_article()()
            else:
                self.view_interesting_news()
        elif selected_menu.startswith("3."):
            # 키워드 추이 확인 또는 기자 변경
            if self.user_type == "admin":
                self.manage_reporters()
            else:
                self.view_keyword_trend()
        elif selected_menu.startswith("4."):
            # 상위 키워드 정보 표시 또는 기자 성실도 체크
            if self.user_type == "admin":
                self.show_reporters_by_monthly_articles()
            else:
                self.view_top_keywords()

    def daily_popular_keywords(self):
        # 날짜 입력 받기 위한 창 생성
        date_input_window = tk.Toplevel()
        date_input_window.title("Enter Date")
        date_input_window.geometry("300x400")
        date_label = tk.Label(date_input_window, text="Enter Date (YYYY-MM-DD):")
        date_label.pack(pady=10)
        date_entry = tk.Entry(date_input_window)
        date_entry.pack(pady=5)
        
        # 람다 함수에서 self.retrieve_keywords 호출
        date_button = tk.Button(date_input_window, text="Submit",
                                command=lambda: self.retrieve_keywords(date_entry.get()))
        date_button.pack(pady=5)
        
    def retrieve_keywords(self, selected_date):
        try:
            self.db.cursor.callproc("GetTopKeywords", [selected_date])
            results = self.db.cursor.fetchall()
    
            if not results:
                messagebox.showinfo("No Data", "No data available for the selected date.")
                return
    
            # 결과를 출력하는 간단한 Tkinter 창 생성
            window = tk.Toplevel()
            window.title(f"Daily Popular Keywords for {selected_date}")
            window.geometry("300x300")
            label = tk.Label(window, text=f"Top Keywords for {selected_date}")
            label.pack(pady=10, expand=True, fill="both")
                
            listbox = tk.Listbox(window)
            for keyword in results:
                # Decimal 값을 문자열로 변환
                keywords = [str(kw) if isinstance(kw, decimal.Decimal) else kw for kw in keyword.values()]
                listbox.insert(tk.END, f"{', '.join(keywords)} (popularity: {keyword['TotalPopularity']})")
    
            listbox.pack(pady=10)
    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # 키워드 별 관심도 높은 뉴스기사 확인 기능을 구현하세요.
    def view_interesting_news(self):
        # 키워드 입력 받기 위한 창 생성
        def search_news_by_keyword(keyword):
            try:
                # 데이터베이스에서 키워드에 해당하는 뉴스 기사 검색
                query = """
                    SELECT Article_ID, Title, Date, Content, Recommendations, Comments
                    FROM Article 
                    WHERE Content LIKE %s
                    ORDER BY (Recommendations + Comments) DESC
                    LIMIT 10
                    """
                self.db.execute(query, (f"%{keyword}%",))
                results = self.db.cursor.fetchall()
    
                if not results:
                    messagebox.showinfo("No Data", f"No articles found containing '{keyword}'.")
                    return
    
                # 검색 결과를 표시하는 Tkinter 창 생성
                result_window = tk.Toplevel()
                result_window.title(f"News Articles for '{keyword}'")
                result_window.geometry("1000x1000")

                frame = tk.Frame(result_window)
                frame.pack(expand=True, fill="both")  # 내부 프레임이 창에 가득 채워지도록 설정
                
                # 레이블 추가
                label = tk.Label(frame, text=f"Articles containing '{keyword}'")
                label.pack(pady=10)

# 리스트박스 크기 조절
                listbox = tk.Listbox(frame)
                for article in results:
                    listbox.insert(tk.END, f"{article['Title']} - {article['Date']}")
                listbox.pack(expand=True, fill="both")  # 리스트박스가 내부 프레임을 가득 채우도록 설정
                    
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
        keyword_input_window = tk.Toplevel()
        keyword_input_window.title("Enter Keyword")
        keyword_input_window.geometry("300x400")
        keyword_label = tk.Label(keyword_input_window, text="Enter Keyword:")
        keyword_label.pack(pady=10)
        keyword_entry = tk.Entry(keyword_input_window)
        keyword_entry.pack(pady=5)
        keyword_button = tk.Button(keyword_input_window, text="Submit",
                                   command=lambda: search_news_by_keyword(keyword_entry.get()))
        keyword_button.pack(pady=5)


    def view_keyword_trend(self):
        # 키워드 별 관심도 추이 확인 기능을 구현하세요.
        # 키워드 입력 받기
        keyword = simpledialog.askstring("Keyword Trend", "Enter keyword:")
        if not keyword:
            messagebox.showinfo("Info", "No keyword entered")
            return

        # 날짜 범위 설정 (2023년 11월 1일부터 11월 30일까지)
        start_date = datetime.date(2023, 11, 1)
        end_date = datetime.date(2023, 11, 30)
        try:
            # 데이터베이스에서 키워드에 해당하는 기사의 추천 및 댓글 수 합산
            query = f"""
                   SELECT Date, SUM(Recommendations + Comments) AS Total_Interactions
                   FROM Article
                   WHERE Content LIKE '%%{keyword}%%'
                     AND Date BETWEEN '{start_date}' AND '{end_date}'
                   GROUP BY Date
                   ORDER BY Date;
                   """

            self.db.execute(query)
            results = self.db.cursor.fetchall()



            # 결과를 그래프로 표시
            dates = [result['Date'] for result in results]
            interactions = [result['Total_Interactions'] for result in results]

            self.plot_trend(dates, interactions, keyword)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def plot_trend(self, dates, interactions, keyword):
        # 그래프 그리기
        fig, ax = plt.subplots()
        ax.plot(dates, interactions, marker='o')
        ax.set(xlabel='Date', ylabel='Total Interactions',
               title = 'Trend of "keyword" Keyword Interactions (Last 30 Days)')
        ax.grid()
        fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        # Tkinter 창에 그래프 표시
        window = tk.Toplevel()
        window.geometry("1000x1000")
        window.title(f"Trend for '{keyword}'")
        canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        pass

    def view_top_keywords(self):
        # 상위 키워드 정보 표시 기능을 구현하세요.
        try:
            # 데이터베이스에서 상위 키워드 검색
            query = '''SELECT Keyword
                        FROM (
                            SELECT Keyword1 AS Keyword FROM Keyword
                            UNION
                            SELECT Keyword2 FROM Keyword
                            UNION
                            SELECT Keyword3 FROM Keyword
                            UNION
                            SELECT Keyword4 FROM Keyword
                            UNION
                            SELECT Keyword5 FROM Keyword
                            UNION
                            SELECT Keyword6 FROM Keyword
                            UNION
                            SELECT Keyword7 FROM Keyword
                        ) AS AllKeywords
                        WHERE Keyword IS NOT NULL
                        GROUP BY Keyword
                        ORDER BY COUNT(Keyword) DESC
                        LIMIT 10
                        '''

            self.db.execute(query)
            results = self.db.cursor.fetchall()

            # 결과를 출력하는 Tkinter 창 생성
            window = tk.Toplevel()
            window.title("Top Keywords")
            window.geometry("300x300")
            label = tk.Label(window, text="Top Keywords")
            label.pack(pady=10)

            listbox = tk.Listbox(window)
            for keyword in results:
                listbox.insert(tk.END, f"{keyword['Keyword']} (popularity: {keyword['TotalPopularity']})")
            listbox.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    def manage_article(self):
        article_management_window = tk.Toplevel()
        article_management_window.title("Article Management")
        article_management_window.geometry("1000x1000")

        def refresh_article_table():
            article_data = self.db.executeAll("SELECT * FROM Article;")
            article_treeview.delete(*article_treeview.get_children())
            for i, article in enumerate(article_data, start=1):
                article_treeview.insert('', 'end', values=(i,) + tuple(article.values()), iid=str(i))

        def on_article_select(event):
            selected_item = article_treeview.selection()
            if selected_item:
                selected_article = article_treeview.item(selected_item, "values")
                article_id_var.set(selected_article[1])
                title_var.set(selected_article[2])
                date_var.set(selected_article[3])
                content_var.set(selected_article[4])
                recommendations_var.set(selected_article[5])
                comments_var.set(selected_article[6])
                press_press_id_var.set(selected_article[7])
                reporter_reporter_id_var.set(selected_article[8])

        def clear_entry_fields():
            article_id_var.set("")
            title_var.set("")
            date_var.set("")
            content_var.set("")
            recommendations_var.set("")
            comments_var.set("")
            press_press_id_var.set("")
            reporter_reporter_id_var.set("")

        def insert_article():
            article_id = article_id_var.get()
            title = title_var.get()
            date = date_var.get()
            content = content_var.get()
            recommendations = recommendations_var.get()
            comments = comments_var.get()
            press_press_id = press_press_id_var.get()
            reporter_reporter_id = reporter_reporter_id_var.get()

            if title and date and content:
                query = "INSERT INTO Article (Article_ID, Title, Date, Content, Recommendations, Comments, Press_Press_ID, Reporter_Reporter_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                args = (
                article_id, title, date, content, recommendations, comments, press_press_id, reporter_reporter_id)
                self.db.update(query, args)
                refresh_article_table()
                clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please fill in all required fields.")

        def update_article():
            article_id = article_id_var.get()
            title = title_var.get()
            date = date_var.get()
            content = content_var.get()
            recommendations = recommendations_var.get()
            comments = comments_var.get()
            press_press_id = press_press_id_var.get()
            reporter_reporter_id = reporter_reporter_id_var.get()

            if article_id and title and date and content:
                query = "UPDATE Article SET Title=%s, Date=%s, Content=%s, Recommendations=%s, Comments=%s, Press_Press_ID=%s, Reporter_Reporter_ID=%s WHERE Article_ID=%s;"
                args = (
                title, date, content, recommendations, comments, press_press_id, reporter_reporter_id, article_id)
                self.db.update(query, args)
                refresh_article_table()
                clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please select an article and fill in all required fields.")

        def delete_article():
            article_id = article_id_var.get()
            if article_id:
                confirm = tkinter.messagebox.askyesno("Delete Article", "Are you sure you want to delete this article?")
                if confirm:
                    self.db.update("DELETE FROM Article WHERE Article_ID=%s;", (article_id,))
                    refresh_article_table()
                    clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please select an article.")

        article_id_var = tk.StringVar()
        title_var = tk.StringVar()
        date_var = tk.StringVar()
        content_var = tk.StringVar()
        recommendations_var = tk.StringVar()
        comments_var = tk.StringVar()
        press_press_id_var = tk.StringVar()
        reporter_reporter_id_var = tk.StringVar()

        article_treeview = ttk.Treeview(article_management_window,
                                        columns=["num", "Article_ID", "Title", "Date", "Content", "Recommendations",
                                                 "Comments", "Press_Press_ID", "Reporter_Reporter_ID"])
        article_treeview.pack()
        article_treeview.column("#0", width=70)
        article_treeview.heading("#0", text="num")
        article_treeview.column("Article_ID", width=70, anchor="w")
        article_treeview.heading("Article_ID", text="Article_ID", anchor="center")
        article_treeview.column("Title", width=100, anchor="w")
        article_treeview.heading("Title", text="Title", anchor="center")
        article_treeview.column("Date", width=100, anchor="w")
        article_treeview.heading("Date", text="Date", anchor="center")
        article_treeview.column("Content", width=100, anchor="w")
        article_treeview.heading("Content", text="Content", anchor="center")
        article_treeview.column("Recommendations", width=100, anchor="w")
        article_treeview.heading("Recommendations", text="Recommendations", anchor="center")
        article_treeview.column("Comments", width=100, anchor="w")
        article_treeview.heading("Comments", text="Comments", anchor="center")
        article_treeview.column("Press_Press_ID", width=100, anchor="w")
        article_treeview.heading("Press_Press_ID", text="Press_Press_ID", anchor="center")
        article_treeview.column("Reporter_Reporter_ID", width=100, anchor="w")
        article_treeview.heading("Reporter_Reporter_ID", text="Reporter_Reporter_ID", anchor="center")
        article_treeview.bind("<ButtonRelease-1>", on_article_select)

        refresh_button = ttk.Button(article_management_window, text="Refresh", command=refresh_article_table)
        refresh_button.pack()

        article_id_label = ttk.Label(article_management_window, text="Article_ID:")
        article_id_label.pack()
        article_id_entry = ttk.Entry(article_management_window, textvariable=article_id_var)
        article_id_entry.pack()

        title_label = ttk.Label(article_management_window, text="Title:")
        title_label.pack()
        title_entry = ttk.Entry(article_management_window, textvariable=title_var)
        title_entry.pack()

        date_label = ttk.Label(article_management_window, text="Date:")
        date_label.pack()
        date_entry = ttk.Entry(article_management_window, textvariable=date_var)
        date_entry.pack()

        content_label = ttk.Label(article_management_window, text="Content:")
        content_label.pack()
        content_entry = ttk.Entry(article_management_window, textvariable=content_var)
        content_entry.pack()

        recommendations_label = ttk.Label(article_management_window, text="Recommendations:")
        recommendations_label.pack()
        recommendations_entry = ttk.Entry(article_management_window, textvariable=recommendations_var)
        recommendations_entry.pack()

        comments_label = ttk.Label(article_management_window, text="Comments:")
        comments_label.pack()
        comments_entry = ttk.Entry(article_management_window, textvariable=comments_var)
        comments_entry.pack()

        press_press_id_label = ttk.Label(article_management_window, text="Press_Press_ID:")

        press_press_id_label.pack()
        press_press_id_entry = ttk.Entry(article_management_window, textvariable=press_press_id_var)
        press_press_id_entry.pack()

        reporter_reporter_id_label = ttk.Label(article_management_window, text="Reporter_Reporter_ID:")
        reporter_reporter_id_label.pack()
        reporter_reporter_id_entry = ttk.Entry(article_management_window, textvariable=reporter_reporter_id_var)
        reporter_reporter_id_entry.pack()

        insert_button = ttk.Button(article_management_window, text="Insert", command=insert_article)
        insert_button.pack()

        update_button = ttk.Button(article_management_window, text="Update", command=update_article)
        update_button.pack()

        delete_button = ttk.Button(article_management_window, text="Delete", command=delete_article)
        delete_button.pack()

        # Initial refresh
        refresh_article_table()

        press_press_id_label = ttk.Label

    def manage_press(self):
        press_management_window = tk.Toplevel()
        press_management_window.title("Press Management")
        press_management_window.geometry("1000x1000")

        # Function to refresh the table
        def refresh_press_table():
            press_data = self.db.executeAll("SELECT * FROM Press;")
            press_treeview.delete(*press_treeview.get_children())  # Clear existing data
            for i, press in enumerate(press_data, start=1):
                press_treeview.insert('', 'end', values=(i,) + tuple(press.values()), iid=str(i))

        # Function to handle the selection in the treeview
        def on_press_select(event):
            selected_item = press_treeview.selection()
            if selected_item:
                selected_press = press_treeview.item(selected_item, "values")
                press_id_var.set(selected_press[1])
                channel_var.set(selected_press[2])
                follownumber_var.set(selected_press[3])

        # Function to clear the entry fields
        def clear_entry_fields():
            press_id_var.set("")
            channel_var.set("")
            follownumber_var.set("")

        # Function to insert a new press
        def insert_press():
            print("Insert Button Clicked")
            press_id = press_id_var.get()
            channel = channel_var.get()
            follownumber = follownumber_var.get()
            if channel and follownumber:
                query = "INSERT INTO Press (Press_ID, Channel, Follownumber) VALUES (%s, %s, %s);"
                args = (press_id, channel, follownumber)
                self.db.update(query, args)
                refresh_press_table()
                clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please fill in all fields.")

        def update_press():
            press_id = press_id_var.get()
            channel = channel_var.get()
            follownumber = follownumber_var.get()
            if press_id and channel and follownumber:
                query = "UPDATE Press SET Channel=%s, Follownumber=%s WHERE Press_ID=%s;"
                args = (channel, follownumber, press_id)
                self.db.update(query, args)
                refresh_press_table()
                clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please select a press and fill in all fields.")

        def delete_press():
            press_id = press_id_var.get()
            channel = channel_var.get()
            follownumber = follownumber_var.get()
            if press_id:
                confirm = tkinter.messagebox.askyesno("Delete Press", "Are you sure you want to delete this press?")
                if confirm:
                    self.db.update("DELETE FROM Press WHERE Press_ID=%s AND Channel=%s AND Follownumber=%s;",
                                   (press_id, channel, follownumber))
                    refresh_press_table()
                    clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please select a press.")

        press_id_var = tk.StringVar()
        channel_var = tk.StringVar()
        follownumber_var = tk.StringVar()

        # Treeview to display press data
        press_treeview = ttk.Treeview(press_management_window, columns=["num", "Press_ID", "Channel", "Follownumber"])
        press_treeview.pack()
        press_treeview.column("#0", width=70)
        press_treeview.heading("#0", text="num")
        press_treeview.column("Press_ID", width=70, anchor="w")
        press_treeview.heading("Press_ID", text="Press_ID", anchor="center")
        press_treeview.column("Channel", width=100, anchor="w")
        press_treeview.heading("Channel", text="Channel", anchor="center")
        press_treeview.column("Follownumber", width=100, anchor="w")
        press_treeview.heading("Follownumber", text="Follownumber", anchor="center")
        press_treeview.bind("<ButtonRelease-1>", on_press_select)

        # Refresh button
        refresh_button = ttk.Button(press_management_window, text="Refresh", command=refresh_press_table)
        refresh_button.pack()

        # Entry fields
        press_id_label = ttk.Label(press_management_window, text="Press_Id:")
        press_id_label.pack()
        press_id_entry = ttk.Entry(press_management_window, textvariable=press_id_var)
        press_id_entry.pack()

        channel_label = ttk.Label(press_management_window, text="Channel:")
        channel_label.pack()
        channel_entry = ttk.Entry(press_management_window, textvariable=channel_var)
        channel_entry.pack()

        follownumber_label = ttk.Label(press_management_window, text="Follownumber:")
        follownumber_label.pack()
        follownumber_entry = ttk.Entry(press_management_window, textvariable=follownumber_var)
        follownumber_entry.pack()

        # Buttons for insert, update, and delete
        insert_button = ttk.Button(press_management_window, text="Insert", command=insert_press)
        insert_button.pack()

        update_button = ttk.Button(press_management_window, text="Update", command=update_press)
        update_button.pack()

        delete_button = ttk.Button(press_management_window, text="Delete", command=delete_press)
        delete_button.pack()

        # Initial refresh
        refresh_press_table()

    def manage_reporters(self):
        reporter_management_window = tk.Toplevel()
        reporter_management_window.title("Reporter Management")
        reporter_management_window.geometry("1000x1000")

        def refresh_reporter_table():
            reporter_data = self.db.executeAll(
                "SELECT Reporter.Reporter_ID, Reporter.Name, COUNT(Article.Article_ID) AS ArticleCount FROM Reporter LEFT JOIN Article ON Reporter.Reporter_ID = Article.Reporter_Reporter_ID GROUP BY Reporter.Reporter_ID, Reporter.Name;")
            reporter_treeview.delete(*reporter_treeview.get_children())
            for i, reporter in enumerate(reporter_data, start=1):
                reporter_treeview.insert('', 'end', values=(i,) + tuple(reporter.values()), iid=str(i))

        def on_reporter_select(event):
            selected_item = reporter_treeview.selection()
            if selected_item:
                selected_reporter = reporter_treeview.item(selected_item, "values")
                reporter_id_var.set(selected_reporter[1])
                name_var.set(selected_reporter[2])

        def clear_entry_fields():
            reporter_id_var.set("")
            name_var.set("")

        def insert_reporter():
            reporter_id = reporter_id_var.get()
            name = name_var.get()

            if reporter_id and name:
                query = "INSERT INTO Reporter (Reporter_ID, Name) VALUES (%s, %s);"
                args = (reporter_id, name)
                self.db.update(query, args)
                refresh_reporter_table()
                clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please fill in all required fields.")

        def update_reporter():
            reporter_id = reporter_id_var.get()
            name = name_var.get()

            if reporter_id and name:
                query = "UPDATE Reporter SET Name=%s WHERE Reporter_ID=%s;"
                args = (name, reporter_id)
                self.db.update(query, args)
                refresh_reporter_table()
                clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please select a reporter and fill in all required fields.")

        def delete_reporter():
            reporter_id = reporter_id_var.get()
            if reporter_id:
                confirm = tkinter.messagebox.askyesno("Delete Reporter",
                                                      "Are you sure you want to delete this reporter?")
                if confirm:
                    self.db.update("DELETE FROM Reporter WHERE Reporter_ID=%s;", (reporter_id,))
                    refresh_reporter_table()
                    clear_entry_fields()
            else:
                tkinter.messagebox.showwarning("Error", "Please select a reporter.")

        reporter_id_var = tk.StringVar()
        name_var = tk.StringVar()

        reporter_treeview = ttk.Treeview(reporter_management_window,
                                         columns=["num", "Reporter_ID", "Name", "ArticleCount"])
        reporter_treeview.pack()
        reporter_treeview.column("#0", width=70)
        reporter_treeview.heading("#0", text="num")
        reporter_treeview.column("Reporter_ID", width=70, anchor="w")
        reporter_treeview.heading("Reporter_ID", text="Reporter_ID", anchor="center")
        reporter_treeview.column("Name", width=100, anchor="w")
        reporter_treeview.heading("Name", text="Name", anchor="center")
        reporter_treeview.column("ArticleCount", width=100, anchor="w")
        reporter_treeview.heading("ArticleCount", text="ArticleCount", anchor="center")
        reporter_treeview.bind("<ButtonRelease-1>", on_reporter_select)

        refresh_button = ttk.Button(reporter_management_window, text="Refresh", command=refresh_reporter_table)
        refresh_button.pack()

        reporter_id_label = ttk.Label(reporter_management_window, text="Reporter_ID:")
        reporter_id_label.pack()
        reporter_id_entry = ttk.Entry(reporter_management_window, textvariable=reporter_id_var)
        reporter_id_entry.pack()

        name_label = ttk.Label(reporter_management_window, text="Name:")
        name_label.pack()
        name_entry = ttk.Entry(reporter_management_window, textvariable=name_var)
        name_entry.pack()

        insert_button = ttk.Button(reporter_management_window, text="Insert", command=insert_reporter)
        insert_button.pack()

        update_button = ttk.Button(reporter_management_window, text="Update", command=update_reporter)
        update_button.pack()

        delete_button = ttk.Button(reporter_management_window, text="Delete", command=delete_reporter)
        delete_button.pack()

        # Initial refresh
        refresh_reporter_table()
    def show_reporters_by_monthly_articles(self):
        try:
            # 기자별 월간 기사 수 및 평균 기사 수 조회 쿼리
            query = """
                SELECT Reporter.Reporter_ID, Reporter.Name, 
                       COALESCE(Reporter.MonthlyArticleWritten, 0) AS MonthlyArticles,
                       CalculateAvgMonthlyArticles() AS AvgMonthlyArticles
                FROM Reporter
                ORDER BY MonthlyArticles ASC;
            """
    
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
    
            if not results:
                messagebox.showinfo("No Data", "No data available for monthly articles.")
                return
    
            # 결과를 출력하는 Tkinter 창 생성
            window = tk.Toplevel()
            window.title("Reporters by Monthly Articles")
            window.geometry("300x300")
    
            label = tk.Label(window, text="Monthly Articles by Reporters with Average")
            label.pack(pady=10, expand=True, fill="both")
    
            listbox = tk.Listbox(window)
            for reporter in results:
                listbox.insert(tk.END, f"{reporter['Name']} - Articles: {reporter['MonthlyArticles']} - Avg: {reporter['AvgMonthlyArticles']}")
    
            listbox.pack(pady=10)
    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


class KeywordApp:
    def __init__(self, master, db):
        self.master = master
        self.master.title("Keyword Service")

        keyword_service = KeywordService(self.authenticate())

        if keyword_service.user_type:
            keyword_service.show_menu()
        else:
            self.master.destroy()

    def authenticate(self):
        # 사용자 인증 및 로그인
        keyword_service = KeywordService(None)
        return keyword_service.authenticate()


# GUI 실행
root = tk.Tk()
app = KeywordApp(root, db)
root.mainloop()
