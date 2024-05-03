import os

OUT_PATH = 'output/'
CHANNELS_PATH = 'bot-inputs/'
USER_AGENT_CSV = 'input/user-agent.csv'
INPUT_RESOLUTION_CSV = 'input/resolution.csv'
COOKIES = "core/cookies"


def get_channel_base_name(channel_name):
    """
    Returns channel videos csv file basename. BASE_DIR/bot-inputs/chans_*
    :param channel_name: Youtube channel name
    :return: Absolute path
    """
    channel_file_name = os.path.join(CHANNELS_PATH, "chans_" + channel_name)
    return get_path(channel_file_name)


def get_cookies():
    """
    Returns path for cookies folder. Cookies folder is critical because it mounted twice when bot is spawned from gui container.
    Therefore its path on the main host machine is store when gui container is created.
    :return: Path of the cookie folder, ready to be used from bot.
    """
    if "COOKIES" in os.environ.keys():
        return os.environ["COOKIES"]
    else:
        return get_path(COOKIES)


def get_path(path):
    """
    Returns absolute directory of the path the base_directory
    :param path:
    :return:
    """
    return os.path.join(os.environ['BASE_DIRECTORY'], path)


def get_gui_output():
    """
    Returns relative path of the output folder to gui folder
    :return: Path
    """
    return os.path.relpath(get_path(OUT_PATH), os.getcwd())


def get_gui_rel_output(name):
    """
    Returns relative path of the file from current path
    :param name:
    :return:
    """
    return os.path.relpath(name, os.getcwd())


def get_output_dir():
    """
    Returns output folder path relative to the base directory
    :return:
    """
    return get_path(OUT_PATH)


def get_output_base_name(file_base_name,store_folder=None):
    """
    Returns base file name of the output file relatively to the base directory
    :param store_folder: custom output folder, default=None
    :param file_base_name:
    :return:
    """
    if store_folder:
        join = os.path.join(store_folder+"/", file_base_name)
    else:
        join = os.path.join(OUT_PATH, file_base_name)
    return get_path(join)


if __name__ == '__main__':
    os.environ['BASE_DIRECTORY'] = os.path.dirname(os.getcwd())

    print(get_gui_rel_output(
        """/home/ali/Development/bot-crawler/output/autoplay-k-"James Hoffmann"-"James Hoffmann"_2_460.csv"""))
