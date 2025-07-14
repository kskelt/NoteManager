from enum import Enum


class Permission(str, Enum):
    CREATE_NOTE = "create_note"
    READ_OWN_NOTE = "read_own_note"
    READ_ALL_NOTES = "read_all_notes"
    READ_USER_NOTES = "read_user_notes"
    UPDATE_OWN_NOTE = "update_own_note"
    DELETE_NOTE = "delete_own_note"
    RESTORE_NOTE = "restore_note"
