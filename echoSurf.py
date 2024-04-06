import time

import pyautogui
import pyperclip
import speech_recognition as sr
import win32con
import win32gui


class ChromeBrowser:
    """
    Handles interactions with the Chrome browser.
    """

    def get_chrome_windows(self):
        """
        Retrieves a list of Chrome windows.

        Returns:
            List of tuples containing window handles and titles.
        """
        chrome_windows = []

        def window_enum_handler(hwnd, result_list):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
                result_list.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(window_enum_handler, chrome_windows)
        chrome_windows = [
            (hwnd, title) for hwnd, title in chrome_windows if "chrome" in title.lower()
        ]
        return chrome_windows

    def switch_to_chrome_tab(self):
        """
        Switches to the first Chrome window, maximizes it, and restores it.
        """
        chrome_windows = self.get_chrome_windows()
        if chrome_windows:
            hwnd, _ = chrome_windows[0]
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            win32gui.SetForegroundWindow(hwnd)


class VoiceCommand(ChromeBrowser):
    """
    Handles voice command recognition and execution.
    """

    def listen_and_convert(self):
        """
        Listens for a voice command using the microphone.

        Returns:
            The recognized voice command, or None if no command is recognized.
        """
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        return None

    def execute_command(self, command):
        """
        Executes the voice command by opening a new Chrome tab and performing a search.

        Args:
            command (str): The voice command to execute.

        Returns:
            bool: True if the command is a shutdown command, False otherwise.
        """
        shutdown_commands = ["SHUTDOWN", "SHUT DOWN", "TERMINATE", "STOP"]
        for shutdown_command in shutdown_commands:
            if shutdown_command in command.upper():
                print("Shutting down...")
                return True
        pyperclip.copy(command)
        self.switch_to_chrome_tab()
        time.sleep(1)
        pyautogui.hotkey("ctrl", "t")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        time.sleep(2)
        return False


if __name__ == "__main__":
    voice_command = VoiceCommand()
    while True:
        command = voice_command.listen_and_convert()
        if command:
            if voice_command.execute_command(command):
                break
