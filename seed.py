from db.database import SessionLocal
from models.user import UserModel
from core.password import handle_hash_password
from models.project import ProjectModel
from models.member import MemberModel
from models.task import TaskModel

def seed_data():
    db = SessionLocal()
    try:
        admin = db.query(UserModel).filter(UserModel.email == "admin01@gmail.com").first()
        if not admin:
            admin = UserModel(
                email="admin01@gmail.com",
                full_name="Nguyễn Anh ADMIN",
                password_hash=handle_hash_password("123456"),
                role="ADMIN",
                is_active=True
            )
            db.add(admin)

        user = db.query(UserModel).filter(UserModel.email == "tunghlls01@gmail.com").first()
        if not user:
            user = UserModel(
                email="tunghlls01@gmail.com",
                full_name="Nguyễn Anh Tùng",
                password_hash=handle_hash_password("123456"),
                role="USER",
                is_active=True
            )
            db.add(user)

        db.commit()
        if admin: db.refresh(admin)
        if user: db.refresh(user)

        project = db.query(ProjectModel).filter(ProjectModel.name == "Quản lý phần mềm AI").first()
        if not project:
            project = ProjectModel(
                name="Quản lý phần mềm AI",
                description="Tra cứu đồ ăn nhanh chóng",
                owner_id=user.id
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            member = MemberModel(
                project_id=project.id,
                user_id=user.id,
                role="MEMBER"
            )
            db.add(member)
            db.commit()
            task = TaskModel(
                project_id=project.id,
                title="Tìm hiểu thị trường món hot",
                description="Liên quan đến app tra món ngon",
                assignee_id=user.id,
                status="TODO"
            )
            db.add(task)
            db.commit()
            print("Seed dữ liệu mẫu thành công!")
        else:
            print("Dữ liệu đề tài mẫu đã tồn tại từ trước.")

    except Exception as e:
        db.rollback()
        print(f"Lỗi khi seed dữ liệu: {e}")
    finally:
        db.close()
if __name__ == "__main__":
    seed_data()