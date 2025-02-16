from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    professors = relationship("Professor", back_populates="department")
    students = relationship("Student", back_populates="department")

class Professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    
    department = relationship("Department", back_populates="professors")
    courses = relationship("Course", back_populates="professor")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    grades = relationship("Grade", back_populates="student")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    professor_id = Column(Integer, ForeignKey('professors.id'))
    
    professor = relationship("Professor", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    grades = relationship("Grade", back_populates="course")

class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    grade = Column(Float, nullable=False)
    
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'student', 'professor', 'admin'

engine = create_engine('sqlite:///university.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


dep1 = Department(name='Computer Science')
dep2 = Department(name='Mathematics')
prof1 = Professor(name='Dr. Smith', department=dep1)
stu1 = Student(name='Alice', department=dep1)
cour1 = Course(name='Data Structures', professor=prof1)
enr1 = Enrollment(student=stu1, course=cour1)
grade1 = Grade(student=stu1, course=cour1, grade=95.0)
user1 = User(name='Alice', email='alice@example.com', password='hashed_password', role='student')
user2 = User(name='Dr. Smith', email='smith@example.com', password='hashed_password', role='professor')

session.add_all([dep1, dep2, prof1, stu1, cour1, enr1, grade1, user1, user2])
session.commit()

print("Database initialized successfully!")
