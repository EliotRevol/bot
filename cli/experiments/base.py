import time
from abc import ABC, abstractmethod

from core.src.bot import runJob
from core.src.user_agent_generator import generate_user_agent_and_resolution
from core.src.utils import dump


class Experiment(ABC):
    """
    All experiments must be inherited from this class.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.args = kwargs
        self.events = None
        self.experiment = kwargs['experiment']

        self.nb_walks = self.args['nb_walks']
        self.nb_runs = self.args['nb_runs']
        self.watchTime = self.args['watch_time']
        if "alea" not in self.args or not self.args["alea"]:
            self.alea = int(self.watchTime / 10)
        else:
            self.alea = self.args["alea"]

        self.lang = self.args['lang']
        self.save_html = self.args['save_html']
        self.cookie = self.args['cookie']
        self.transcript_language = self.args['transcript_language']
        self.store_folder=self.args['store_folder']
    def run_and_dump(self, events, filename):
        """
        Runs the bot container and saves results.
        :param events: Bot events
        :param filename: filename prefix to save files
        """
        result = runJob(events, generate_user_agent_and_resolution(), self.cookie, self.lang, self.save_html)
        dump(globals(), result, filename, self.save_html, self.cookie, self.transcript_language,self.store_folder)

    @abstractmethod
    def run(self):
        """
        Abstract method for running experiment
        :return:
        """


class ElectionExperiment(Experiment, ABC):
    """
    Abstract class for election experiment
    """


class GenericExperiment(Experiment, ABC):
    """
    Abstract class for generic experiment.
    """


class ExperimentUnsetSettings(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ExperimentNotFound(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_timestamp():
    return str(time.time()).split('.')[0]
