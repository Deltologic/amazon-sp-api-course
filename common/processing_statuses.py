from enum import Enum


class ProcessingStatus(Enum):
    DONE="DONE"
    CANCELLED = "CANCELLED"
    FATAL="FATAL"
    IN_PROGRESS="IN_PROGRESS"
    IN_QUEUE="IN_QUEUE"
