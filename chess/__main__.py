"""This file is the main laucher for the chess tournament application"""
# from chess.controllers.main_controller import ApplicationController
from chess.controllers.main_controller import MainController

from colorama import init


def main():
    """This is the main function of the application"""
    init()
    controller = MainController()
    controller.run()


if __name__ == '__main__':
    main()
