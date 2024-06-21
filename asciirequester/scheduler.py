import datetime
import sys
import time


class Scheduler:
    def __init__(self):
        """
        Initialize Scheduler. The schedule is used to run some task indefinitely

        Determines delay for the specific task based on the ISO week number.
        """
        self.delay = self.get_delay_in_seconds()

    def get_iso_week(self):
        """
        Get ISO week number of the current date.

        Returns:
        int: ISO week number.
        """
        today = datetime.date.today()
        _, iso_week, _ = today.isocalendar()
        return iso_week

    def get_delay_in_seconds(self):
        """
        Get delay in seconds based on ISO week number.

        Returns:
        int: Delay in seconds.
        """
        if self.get_iso_week() % 2 == 0:
            return 10
        return 5

    def schedule_task(self, job):
        """
        Schedule a task with a job.

        The job is executed repeatedly with a delay determined by the ISO week number.

        Parameters:
        job: The job to be scheduled.
        """
        while True:
            try:
                job.schedule_task()
            except Exception as e:
                print("Job Failed with Exception: ", e)
                break
            sys.stdout.flush()
            time.sleep(self.delay)
