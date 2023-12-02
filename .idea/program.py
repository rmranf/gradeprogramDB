import cx_Oracle

dsn = cx_Oracle.makedsn(host='localhost', port="", sid='')
username = ''
password = ''

# 데이터베이스 연결
connection = cx_Oracle.connect(username, password, dsn)
cursor = connection.cursor()
#학생 정보 출력
def find_student(student_id):
    # 학생 테이블에서 학번으로 학생 정보 조회
    cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
    student_info = cursor.fetchone()

    if student_info is None:
        print("해당 학생이 데이터베이스에 존재하지 않습니다.")
    else:
        # 학생의 과목과 점수, 학점 조회
        cursor.execute("SELECT Subjects.SubjectName, Grades.Score, Grades.GradeLetter FROM Subjects JOIN Grades ON Subjects.SubjectID = Grades.SubjectID WHERE Grades.StudentID = :student_id", student_id=student_id)
        subjects = cursor.fetchall()

        print(f"학생 정보: {student_info}")
        for subject in subjects:
            print(f"과목: {subject[0]} 점수: {subject[1]}, 학점: {subject[2]}")
# 학생 정보 수정 함수
def update_student(student_id):
    # 학생 테이블에서 학번으로 학생 정보 조회
    cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
    student_info = cursor.fetchone()

    if student_info is None:
        print("해당 학생이 데이터베이스에 존재하지 않습니다.")
        return

    print(f"현재 학생 정보: {student_info}")

    # 수정할 정보 입력 받기
    name = input("수정할 학생의 이름을 입력하세요: ")
    age = input("수정할 학생의 나이를 입력하세요: ")
    major = input("수정할 학생의 전공을 입력하세요: ")

    try:
        # 학생 정보 수정 쿼리
        sql = "UPDATE Students SET Name = :name, Age = :age, Major = :major WHERE StudentID = :student_id"
        cursor.execute(sql, name=name, age=age, major=major, student_id=student_id)
        connection.commit()
        print("학생 정보 수정이 완료되었습니다.")
    except cx_Oracle.DatabaseError as e:
        print(f"데이터베이스 오류: {e}")

def show_all_students():
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()

    if len(students) == 0:
        print("등록된 학생이 없습니다.")
    else:
        print("전체 학생 데이터:")
        for student in students:
            print(student)

# 성적 등록 함수
def add_grade(student_id):
    # 과목 테이블에서 과목 목록 조회
    cursor.execute("SELECT * FROM Subjects")
    subjects = cursor.fetchall()

    if len(subjects) == 0:
        print("등록된 과목이 없습니다.")
        return

    print("등록 가능한 과목 목록:")
    for subject in subjects:
        subject_id, subject_name, _ = subject  # 과목 정보에서 필요한 부분만 가져오기
        print(f"{subject_id}: {subject_name}")

    subject_id = input("과목 코드를 입력하세요: ")

    # 입력한 과목 코드가 유효한지 확인
    valid_subject = False
    for subject in subjects:
        if subject[0] == subject_id:
            valid_subject = True
            break

    if not valid_subject:
        print("유효하지 않은 과목 코드입니다.")
        return

    # 학생이 이미 해당 과목의 성적을 등록한 경우 중복 등록 방지
    cursor.execute("SELECT * FROM Grades WHERE StudentID = :student_id AND SubjectID = :subject_id",
                   student_id=student_id, subject_id=subject_id)
    existing_grade = cursor.fetchone()

    if existing_grade is not None:
        print("이미 해당 과목의 성적을 등록하였습니다.")
        return

    # 문자열로 된 점수를 입력받기
    score_str = input("점수를 입력하세요: ")

    try:
        # 입력받은 문자열을 실수로 변환
        score = float(score_str)
    except ValueError as e:
        print(f"점수는 숫자로 입력해야 합니다. 에러: {e}")
        return

    # 학점을 문자열로 입력받기
    grade_letter = input("학점을 입력하세요: ")

    print(f"입력된 점수: {score}")

    try:
        # 성적 등록 쿼리
        sql = "INSERT INTO Grades (StudentID, SubjectID, Score, GradeLetter) VALUES (:student_id, :subject_id, :score, :grade_letter)"
        cursor.execute(sql, student_id=student_id, subject_id=subject_id, score=score, grade_letter=grade_letter)
        connection.commit()
        print("성적 등록이 완료되었습니다.")
    except cx_Oracle.DatabaseError as e:
        print(f"데이터베이스 오류: {e}")


#학생데이터 삭제
def delete_student(student_id):
    # 학생 테이블에서 학번으로 학생 정보 조회
    cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
    student_info = cursor.fetchone()

    if student_info is None:
        print("해당 학생이 데이터베이스에 존재하지 않습니다.")
    else:
        try:
            # 학생 정보 삭제 쿼리
            cursor.execute("DELETE FROM Students WHERE StudentID = :student_id", student_id=student_id)
            connection.commit()
            print("학생 정보 삭제가 완료되었습니다.")
        except cx_Oracle.DatabaseError as e:
            print(f"데이터베이스 오류: {e}")
# 과목 추가 함수
def add_subject():
    subject_id = input("과목 코드를 입력하세요: ")

    # 입력한 과목 코드가 이미 존재하는지 확인
    cursor.execute("SELECT * FROM Subjects WHERE SubjectID = :subject_id", subject_id=subject_id)
    existing_subject = cursor.fetchone()

    if existing_subject is not None:
        print("이미 해당 과목 코드가 존재합니다.")
        return

    subject_name = input("과목 이름을 입력하세요: ")

    try:
        # 과목 추가 쿼리
        sql = "INSERT INTO Subjects (SubjectID, SubjectName) VALUES (:subject_id, :subject_name)"
        cursor.execute(sql, subject_id=subject_id, subject_name=subject_name)
        connection.commit()
        print("과목 추가가 완료되었습니다.")
    except cx_Oracle.DatabaseError as e:
        print(f"데이터베이스 오류: {e}")


# 성적 수정 함수
def update_grade(student_id):
    # 학생 테이블에서 학번으로 학생 정보 조회
    cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
    student_info = cursor.fetchone()

    if student_info is None:
        print("해당 학생이 데이터베이스에 존재하지 않습니다.")
        return

    print(f"현재 학생 정보: {student_info}")

    # 수정할 과목 코드 입력 받기
    subject_id = input("수정할 성적의 과목 코드를 입력하세요: ")

    # 입력한 과목 코드가 유효한지 확인
    cursor.execute("SELECT * FROM Subjects WHERE SubjectID = :subject_id", subject_id=subject_id)
    subject_info = cursor.fetchone()

    if subject_info is None:
        print("유효하지 않은 과목 코드입니다.")
        return

    # 현재 과목의 성적 조회
    cursor.execute("SELECT * FROM Grades WHERE StudentID = :student_id AND SubjectID = :subject_id", student_id=student_id, subject_id=subject_id)
    grade_info = cursor.fetchone()

    if grade_info is None:
        print("해당 학생의 해당 과목 성적이 존재하지 않습니다.")
        return

    print(f"현재 성적: {grade_info[2]}")

    # 수정할 성적 입력 받기
    new_score_str = input("수정할 성적을 입력하세요 (변경하지 않으려면 엔터를 누르세요): ")
    if new_score_str == "":
        new_score = grade_info[2]  # 기존 성적 유지
    else:
        try:
            new_score = float(new_score_str)
        except ValueError as e:
            print(f"성적은 숫자로 입력해야 합니다. 에러: {e}")
            return

    # 수정할 학점 입력 받기
    new_grade = input("수정할 학점을 입력하세요 (변경하지 않으려면 엔터를 누르세요): ")
    if new_grade == "":
        new_grade = grade_info[3]  # 기존 학점 유지

    try:
        # 성적 수정 쿼리
        sql = "UPDATE Grades SET Score = :new_score, GradeLetter = :new_grade WHERE StudentID = :student_id AND SubjectID = :subject_id"
        cursor.execute(sql, new_score=new_score, new_grade=new_grade, student_id=student_id, subject_id=subject_id)
        connection.commit()
        print("성적 수정이 완료되었습니다.")
    except cx_Oracle.DatabaseError as e:
        print(f"데이터베이스 오류: {e}")

# 학생 등록 함수
def add_student():
    student_id = input("학번을 입력하세요: ")

    # 학생 테이블에서 학번으로 학생 정보 조회
    cursor.execute("SELECT * FROM Students WHERE StudentID = :student_id", student_id=student_id)
    student_info = cursor.fetchone()

    if student_info is not None:
        print("이미 동일한 학번이 존재합니다.")
        return

    name = input("학생의 이름을 입력하세요: ")
    age = input("학생의 나이를 입력하세요: ")
    major = input("학생의 전공을 입력하세요: ")
    try:
        # 학생 등록 쿼리
        sql = "INSERT INTO Students (StudentID, Name, Age, Major) VALUES (:student_id, :name, :age, :major)"
        cursor.execute(sql, student_id=student_id, name=name, age=age, major=major)
        connection.commit()
        print("학생 등록이 완료되었습니다.")
    except cx_Oracle.DatabaseError as e:
        print(f"데이터베이스 오류: {e}")

# 메인 함수
def main():
    while True:
        print("0: 학생 정보 삭제")
        print("1: 학생 정보 찾기")
        print("2: 학생 등록")
        print("3: 학생 정보 수정")
        print("4: 성적 등록")
        print("5: 과목 추가")
        print("6: 성적 수정")
        print("7: 전체 학생 정보")
        print("8: 종료")
        choice = input("원하는 작업을 선택하세요: ")

        if choice == "1":
            student_id = input("찾을 학생의 학번을 입력하세요: ")
            find_student(student_id)
        elif choice == "2":
            add_student()
        elif choice == "3":
            student_id = input("정보를 수정할 학생의 학번을 입력하세요: ")
            update_student(student_id)
        elif choice == "4":
            student_id = input("성적을 등록할 학생의 학번을 입력하세요: ")
            add_grade(student_id)
        elif choice == "5":
            add_subject()
        elif choice == "6":
            student_id = input("성적을 수정할 학생의 학번을 입력하세요: ")
            update_grade(student_id)
        elif choice == "7":
            show_all_students()

        elif choice == "8":
            break
        elif choice == "0":
            student_id = input("삭제할 학생의 학번을 입력하세요: ")
            delete_student(student_id)

        else:
            print("잘못된 선택입니다.")

    # 데이터베이스 연결 종료
    cursor.close()
    connection.close()

# 메인 함수 호출
if __name__ == "__main__":
    main()