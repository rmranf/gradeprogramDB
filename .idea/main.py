import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

import cx_Oracle
class 학생관리시스템GUI:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection


        title_label = tk.Label(root, text="학생 관리 시스템", font=("Helvetica", 20))
        self.bg_image = tk.PhotoImage(file="20230508034734.jpg")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        # 버튼 생성 및 크기 설정
        btn_width = 8
        btn_height = 2

        self.btn_find_student = tk.Button(root, text="학생 찾기", command=self.find_student, width=btn_width, height=btn_height)
        self.btn_add_student = tk.Button(root, text="학생 등록", command=self.add_student, width=btn_width, height=btn_height)
        self.btn_update_student = tk.Button(root, text="학생 수정", command=self.update_student, width=btn_width, height=btn_height)
        self.btn_add_grade = tk.Button(root, text="성적 등록", command=self.add_grade, width=btn_width, height=btn_height)
        self.btn_add_subject = tk.Button(root, text="과목 추가", command=self.add_subject, width=btn_width, height=btn_height)
        self.btn_update_grade = tk.Button(root, text="성적 수정", command=self.update_grade, width=btn_width, height=btn_height)
        self.btn_show_all_students = tk.Button(root, text="전체 학생 정보", command=self.show_all_students, width=btn_width, height=btn_height)
        self.btn_delete_student = tk.Button(root, text="학생 삭제", command=self.delete_student, width=btn_width, height=btn_height)
        self.btn_exit = tk.Button(root, text="종료", command=root.destroy, width=btn_width, height=btn_height)

        # 타이틀 레이블을 중앙에 배치
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # 그리드에 버튼 배치 (중앙에 배치하고 위아래로 간격을 두기)
        self.btn_find_student.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.btn_add_student.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.btn_update_student.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.btn_add_grade.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.btn_add_subject.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.btn_update_grade.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        self.btn_show_all_students.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.btn_delete_student.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
        self.btn_exit.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")

        # 그리드의 행과 열 가중치 설정 (중앙 정렬을 위한 설정)
        self.root.grid_rowconfigure(0, weight=1)
        for i in range(1, 7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)
        # 그리드의 행과 열 가중치 설정 (중앙 정렬을 위한 설정)



    def find_student(self):
        student_id = simpledialog.askstring("학생 찾기", "찾을 학생의 학번을 입력하세요:")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
                student_info = cursor.fetchone()

            if student_info is not None:
                messagebox.showinfo("학생 찾기", f"학번: {student_info[0]}\n이름: {student_info[1]}\n나이: {student_info[2]}\n전공: {student_info[3]}")
            else:
                messagebox.showinfo("학생 찾기", "학생이 데이터베이스에 존재하지 않습니다.")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("데이터베이스 오류", f"데이터베이스 접근 중 오류 발생: {e}")

    def add_student(self):
        student_id = simpledialog.askstring("학생 등록", "학번을 입력하세요:")

        # Check if the student with the given ID already exists
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
            existing_student = cursor.fetchone()

        if existing_student:
            messagebox.showinfo("학생 등록", "이미 등록된 학생입니다.")
        else:
            name = simpledialog.askstring("학생 등록", "학생의 이름을 입력하세요:")
            age = simpledialog.askstring("학생 등록", "학생의 나이를 입력하세요:")
            major = simpledialog.askstring("학생 등록", "학생의 전공을 입력하세요:")

            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO Students (StudentID, Name, Age, Major) VALUES (:student_id, :name, :age, :major)",
                                   student_id=student_id, name=name, age=age, major=major)
                    self.connection.commit()

                messagebox.showinfo("학생 등록", "학생 등록이 완료되었습니다.")

            except cx_Oracle.DatabaseError as e:
                messagebox.showerror("데이터베이스 오류", f"데이터베이스 접근 중 오류 발생: {e}")

    def update_student(self):
        student_id = simpledialog.askstring("학생 수정", "정보를 수정할 학생의 학번을 입력하세요:")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
                student_info = cursor.fetchone()

            if student_info is not None:
                print(f"현재 학생 정보: {student_info}")
                name = simpledialog.askstring("학생 수정", "수정할 학생의 이름을 입력하세요:")
                age = simpledialog.askstring("학생 수정", "수정할 학생의 나이를 입력하세요:")
                major = simpledialog.askstring("학생 수정", "수정할 학생의 전공을 입력하세요:")

                with self.connection.cursor() as cursor:
                    cursor.execute("UPDATE Students SET Name = :name, Age = :age, Major = :major WHERE StudentID = :student_id",
                                   name=name, age=age, major=major, student_id=student_id)
                    self.connection.commit()

                messagebox.showinfo("학생 정보 수정", "학생 정보 수정이 완료되었습니다.")
            else:
                messagebox.showinfo("학생 정보 수정", "해당 학생이 데이터베이스에 존재하지 않습니다.")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("데이터베이스 오류", f"데이터베이스 접근 중 오류 발생: {e}")

    def add_grade(self):
        student_id = simpledialog.askstring("성적 등록", "성적을 등록할 학생의 학번을 입력하세요:")
        subject_id = simpledialog.askstring("성적 등록", "과목 코드를 입력하세요:")
        score_str = simpledialog.askstring("성적 등록", "점수를 입력하세요:")


        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO Grades (StudentID, SubjectID, Score) VALUES (:student_id, :subject_id, :score)",
                               student_id=student_id, subject_id=subject_id, score=score_str)
                self.connection.commit()

            messagebox.showinfo("성적 등록", "성적 등록이 완료되었습니다.")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("데이터베이스 오류", f"데이터베이스 접근 중 오류 발생: {e}")

    def add_subject(self):
        subject_id = simpledialog.askstring("과목 추가", "과목 코드를 입력하세요:")
        subject_name = simpledialog.askstring("과목 추가", "과목 이름을 입력하세요:")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO Subjects (SubjectID, SubjectName) VALUES (:subject_id, :subject_name)",
                               subject_id=subject_id, subject_name=subject_name)
                self.connection.commit()

            messagebox.showinfo("과목 추가", "과목 추가가 완료되었습니다.")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("데이터베이스 오류", f"데이터베이스 접근 중 오류 발생: {e}")

    def update_grade(self):
        student_id = simpledialog.askstring("성적 수정", "성적을 수정할 학생의 학번을 입력하세요:")
        subject_id = simpledialog.askstring("성적 수정", "성적을 수정할 과목 코드를 입력하세요:")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
                student_info = cursor.fetchone()

                if student_info is not None:
                    cursor.execute("SELECT * FROM Subjects WHERE SubjectID = :subject_id", subject_id=subject_id)
                    subject_info = cursor.fetchone()

                    if subject_info is not None:
                        cursor.execute("SELECT * FROM Grades WHERE StudentID = :student_id AND SubjectID = :subject_id",
                                       student_id=student_id, subject_id=subject_id)
                        grade_info = cursor.fetchone()

                        if grade_info is not None:
                            print(f"현재 성적: {grade_info[2]}")
                            new_score_str = simpledialog.askstring("성적 수정", "수정할 성적을 입력하세요 (변경하지 않으려면 엔터를 누르세요): ")

                            if new_score_str == "":
                                new_score = grade_info[2]  # 기존 성적 유지
                            else:
                                new_score = float(new_score_str)

                            new_grade = simpledialog.askstring("성적 수정", "수정할 학점을 입력하세요 (변경하지 않으려면 엔터를 누르세요): ")

                            if new_grade == "":
                                new_grade = grade_info[3]  # 기존 학점 유지

                            with self.connection.cursor() as cursor:
                                cursor.execute("UPDATE Grades SET Score = :new_score, GradeLetter = :new_grade WHERE StudentID = :student_id AND SubjectID = :subject_id",
                                               new_score=new_score, new_grade=new_grade, student_id=student_id, subject_id=subject_id)
                                self.connection.commit()

                            messagebox.showinfo("성적 수정", "성적 수정이 완료되었습니다.")

                        else:
                            messagebox.showinfo("성적 수정", "해당 학생의 해당 과목 성적이 존재하지 않습니다.")
                    else:
                        messagebox.showinfo("성적 수정", "유효하지 않은 과목 코드입니다.")
                else:
                    messagebox.showinfo("성적 수정", "해당 학생이 데이터베이스에 존재하지 않습니다.")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("데이터베이스 오류", f"데이터베이스 접근 중 오류 발생: {e}")

    def show_all_students(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Students")
                students = cursor.fetchall()

            if len(students) == 0:
                messagebox.showinfo("전체 학생 정보", "등록된 학생이 없습니다.")
            else:
                all_students_info = "전체 학생 데이터:\n"
                for student in students:
                    all_students_info += f"{student}\n"

                messagebox.showinfo("전체 학생 정보", all_students_info)

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("데이터베이스 오류", f"데이터베이스 접근 중 오류 발생: {e}")

    def delete_student(self):
        student_id = simpledialog.askstring("학생 삭제", "삭제할 학생의 학번을 입력하세요:")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
                student_info = cursor.fetchone()

                if student_info is not None:
                    cursor.execute("DELETE FROM Students WHERE StudentID = :student_id", student_id=student_id)
                    self.connection.commit()

                    messagebox.showinfo("학생 삭제", "학생 정보 삭제가 완료되었습니다.")
                else:
                    messagebox.showinfo("학생 삭제", "해당 학생이 데이터베이스에 존재하지 않습니다.")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("데이터베이스 오류", f"데이터베이스 접근 중 오류 발생: {e}")

if __name__ == "__main__":

    # 데이터베이스 연결 정보
    dsn = cx_Oracle.makedsn(host='localhost', port='', sid='xe')
    username = ''
    password = ''

    # 데이터베이스 연결
    try:
        connection = cx_Oracle.connect(username, password, dsn)
    except cx_Oracle.DatabaseError as e:
        print(f"데이터베이스에 연결할 수 없습니다: {e}")
        exit()

    root = tk.Tk()
    app = 학생관리시스템GUI(root, connection)
    root.geometry("1800x2000")
    root.mainloop()

    # 데이터베이스 연결 종료
    connection.close()

