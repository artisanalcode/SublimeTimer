import sublime
import sublime_plugin
import datetime


class Timer:
    timer_count = None
    timer_status = 0  # 0: stopped | 1: started | 2: paused

    def update_status_bar(self):
        if self.timer_count.hour > 12:
            self.stop_timer()
            sublime.status_message("12:00:00 Reached!")
        else:
            sublime.status_message("Timer: %02d:%02d:%02d " % (
                                   self.timer_count.hour,
                                   self.timer_count.minute,
                                   self.timer_count.second))

    def tick(self):
        # Is empty
        if not self.timer_count:
            return

        # Is stopped
        if self.timer_status == 0:
            return

        # Is paused
        elif self.timer_status == 2:
            self.update_status_bar()
            sublime.set_timeout(self.tick, 1000)
            return

        self.timer_count += datetime.timedelta(seconds=1)

        self.update_status_bar()

        # Is running
        if self.timer_status == 1:
            sublime.set_timeout(self.tick, 1000)

    def start_timer(self):
        # 2012: Good enough for the Mayans!
        self.timer_count = datetime.datetime(2012, 1, 1, 0)
        self.timer_status = 1
        sublime.set_timeout(self.tick, 1000)

    def pause_timer(self):
        if self.timer_status == 2:
            self.timer_status = 1
        else:
            self.timer_status = 2

    def stop_timer(self):
        self.timer_status = 0
        self.timer_count = 0

timer = Timer()


class StartTimerCommand(sublime_plugin.WindowCommand):
    def run(self):
        timer.start_timer()


class PauseTimerCommand(sublime_plugin.WindowCommand):
    def run(self):
        timer.pause_timer()


class StopTimerCommand(sublime_plugin.WindowCommand):
    def run(self):
        timer.stop_timer()
