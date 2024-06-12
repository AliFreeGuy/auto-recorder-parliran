# from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime

# Base = declarative_base()

# class Recorder(Base):
#     __tablename__ = 'recorders'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user = Column(String, nullable=False)
#     start_time = Column(String, nullable=False)
#     end_time = Column(String, nullable=False)
#     date_time = Column(DateTime, nullable=False)
#     status = Column(String, nullable=False)
#     file_path = Column(String, nullable=False)
#     file_id = Column(String, nullable=False)
#     file_size = Column(Integer, nullable=False)
#     task_id = Column(String, nullable=False)

# class Database:
#     def __init__(self, db_url='sqlite:///recorders.db'):
#         self.engine = create_engine(db_url)
#         Base.metadata.create_all(self.engine)
#         self.Session = sessionmaker(bind=self.engine)
    
#     def session(self):
#         return self.Session()


# db = Database().session()

# # ایجاد یک سشن

# # # ایجاد یک رکورد جدید
# # new_recorder = Recorder(
# #     user='JohnDoe',
# #     start_time=datetime(2024, 6, 11, 10, 0),
# #     end_time=datetime(2024, 6, 11, 11, 0),
# #     date_time=datetime.now(),
# #     status='active',
# #     file_path='/path/to/file',
# #     file_id='file123',
# #     file_size=1024,
# #     task_id='task123'
# # )

# # session.add(new_recorder)
# # session.commit()
# # print(f"New recorder added with ID: {new_recorder.id}")

# # # خواندن تمام رکوردها
# # recorders = session.query(Recorder).all()

# # # چاپ داده‌ها
# # for recorder in recorders:
# #     print(f"ID: {recorder.id}, User: {recorder.user}, Start Time: {recorder.start_time}, End Time: {recorder.end_time}, Date Time: {recorder.date_time}, Status: {recorder.status}, File Path: {recorder.file_path}, File ID: {recorder.file_id}, File Size: {recorder.file_size}, Task ID: {recorder.task_id}")

# # # به‌روزرسانی یک رکورد
# # recorder_to_update = session.query(Recorder).filter_by(id=new_recorder.id).first()

# # if recorder_to_update:
# #     recorder_to_update.status = 'completed'
# #     session.commit()
# #     print(f"Recorder with ID {recorder_to_update.id} updated successfully")
# # else:
# #     print("Recorder not found")

# # # حذف یک رکورد
# # recorder_to_delete = session.query(Recorder).filter_by(id=new_recorder.id).first()

# # if recorder_to_delete:
# #     session.delete(recorder_to_delete)
# #     session.commit()
# #     print(f"Recorder with ID {recorder_to_delete.id} deleted successfully")
# # else:
# #     print("Recorder not found")
