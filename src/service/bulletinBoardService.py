from database.orm import BulletinBoard


class BulletinBoardService:

    def replace_field(self, bulletinBoard: BulletinBoard) -> BulletinBoard:
        if bulletinBoard.updated_at is None:
            bulletinBoard.updated_at = ""

        if not bulletinBoard.user.is_active:
            bulletinBoard.user.username = "탈퇴한 유저"
        return bulletinBoard